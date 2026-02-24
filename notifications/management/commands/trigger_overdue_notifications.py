from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from shipments.models import Shipment
from payments.models import Payment
from notifications.knock_client import trigger_notification
from notifications.knock_recipients import get_role_recipients

class Command(BaseCommand):
    help = 'Triggers Knock notifications for overdue payments and late shipments.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        self.stdout.write("Starting overdue notification triggers...")

        # ── 1. Overdue Payments ──────────────────────────────────────────────
        overdue_payments = Payment.objects.filter(
            expected_payment_date__lt=today,
            actual_payment_date__isnull=True
        ).select_related("entered_by", "sale", "sale__shipment")

        # Role-based in-app recipients: Admin + Finance Agent + Sales Agent
        role_recipients = get_role_recipients()

        # Always include the fixed email address (inline Knock recipient)
        email_recipient = {
            "id": "khalfanathman12@gmail.com",
            "email": "khalfanathman12@gmail.com",
            "name": "Khalfan",
        }

        payment_count = 0
        for payment in overdue_payments:
            days_overdue = (today - payment.expected_payment_date).days
            user = payment.entered_by
            if user:
                actor_id = str(user.id)
                company_name = payment.sale.shipment.country_origin if payment.sale and payment.sale.shipment else "N/A"
                amount_payed = str(payment.amount_paid)
                amount_due = str(payment.sale.total_sale_amount) if payment.sale else "N/A"
                user_name = user.full_name or user.username

                # Merge role recipients + entered_by user + the email recipient (deduplicate IDs)
                all_ids = list(set(role_recipients + [actor_id]))
                recipients = all_ids + [email_recipient]

                trigger_notification(
                    workflow_key="payment-overdue",
                    recipients=recipients,
                    actor=actor_id,
                    data={
                        "company_name": company_name,
                        "user": {"name": user_name},
                        "amount_payed": amount_payed,
                        "amount_due": amount_due,
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

        # For shipments, notify all role-based users (Admin + Finance + Sales)
        shipment_recipients = get_role_recipients()

        late_count = 0
        soon_count = 0
        for shipment in in_transit:
            estimated_arrival = (
                shipment.created_at.date()
                + timedelta(days=shipment.estimated_transit_days)
            )
            days_diff = (estimated_arrival - today).days
            short_id = str(shipment.id)[:8].upper()

            if days_diff < 0:
                trigger_notification(
                    workflow_key="shipment_late",
                    recipients=shipment_recipients,
                    data={
                        "shipment_id": short_id,
                        "country_origin": shipment.country_origin,
                        "days_past": abs(days_diff),
                    }
                )
                late_count += 1
            elif days_diff <= 2:
                label = "today" if days_diff == 0 else f"in {days_diff} day{'s' if days_diff != 1 else ''}"
                trigger_notification(
                    workflow_key="shipment_arriving",
                    recipients=shipment_recipients,
                    data={
                        "shipment_id": short_id,
                        "country_origin": shipment.country_origin,
                        "arriving_label": label,
                    }
                )
                soon_count += 1

        self.stdout.write(self.style.SUCCESS(f"Triggered {late_count} late and {soon_count} arriving soon shipment notifications."))
