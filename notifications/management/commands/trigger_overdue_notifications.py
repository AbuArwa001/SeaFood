import { BaseCommand } from 'django.core.management.base'
from django.utils import timezone
from datetime import timedelta
from shipments.models import Shipment
from payments.models import Payment
from notifications.knock_client import trigger_notification

class Command(BaseCommand):
    help = 'Triggers Knock notifications for overdue payments and late shipments.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        self.stdout.write("Starting overdue notification triggers...")

        # ── 1. Overdue Payments ──────────────────────────────────────────────
        overdue_payments = Payment.objects.filter(
            expected_payment_date__lt=today,
            actual_payment_date__isnull=True
        ).select_related("entered_by")

        payment_count = 0
        for payment in overdue_payments:
            days_overdue = (today - payment.expected_payment_date).days
            user = payment.entered_by
            if user:
                trigger_notification(
                    workflow_key="payment_overdue",
                    recipients=[str(user.id)],
                    data={
                        "buyer_name": payment.buyer_name,
                        "days_overdue": days_overdue,
                        "payment_id": str(payment.id),
                    }
                )
                payment_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Triggered {payment_count} payment overdue notifications."))

        # ── 2. Shipments IN_TRANSIT ──────────────────────────────────────────
        in_transit = Shipment.objects.filter(
            status="IN_TRANSIT",
            estimated_transit_days__isnull=False,
        )

        late_count = 0
        soon_count = 0
        for shipment in in_transit:
            estimated_arrival = (
                shipment.created_at.date()
                + timedelta(days=shipment.estimated_transit_days)
            )
            days_diff = (estimated_arrival - today).days
            short_id = str(shipment.id)[:8].upper()

            # For now, let's notify the creator of the shipment, assuming shipment 
            # might not have an entered_by. We notify Admin role users as fallback since 
            # SeaFood app typically requires admin or specific agents. 
            # In a production app, we'd loop over active admins/agents.
            # We'll send to a mock object or you can fetch Admin users.
            from users.models import User
            admins = list(User.objects.filter(role__role_name="Admin").values_list('id', flat=True))
            recipients = [str(aid) for aid in admins]

            if days_diff < 0:
                trigger_notification(
                    workflow_key="shipment_late",
                    recipients=recipients,
                    data={
                        "shipment_id": short_id,
                        "country_origin": shipment.country_origin,
                        "days_past": abs(days_diff),
                    }
                )
                late_count += 1
            elif days_diff <= 2:
                # Arriving soon
                label = "today" if days_diff == 0 else f"in {days_diff} day{'s' if days_diff != 1 else ''}"
                trigger_notification(
                    workflow_key="shipment_arriving",
                    recipients=recipients,
                    data={
                        "shipment_id": short_id,
                        "country_origin": shipment.country_origin,
                        "arriving_label": label,
                    }
                )
                soon_count += 1

        self.stdout.write(self.style.SUCCESS(f"Triggered {late_count} late and {soon_count} arriving soon shipment notifications."))
