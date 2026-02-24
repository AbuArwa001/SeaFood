from rest_framework import permissions, viewsets
from .models import Payment
from .serializers import PaymentSerializer
from users.permissions import IsFinanceAgent, IsOwnerOrAdmin
from users.models import User


class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing payment instances.
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsFinanceAgent, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return Payment.objects.all()
        return Payment.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)

    def perform_update(self, serializer):
        # Detect if actual_payment_date is being set (payment is being completed)
        old_instance = self.get_object()
        was_paid = old_instance.actual_payment_date is not None

        instance = serializer.save()

        # Only fire if actual_payment_date is newly set (payment just completed)
        is_now_paid = instance.actual_payment_date is not None
        if not was_paid and is_now_paid:
            try:
                from notifications.knock_client import trigger_notification

                # Get all admin users to notify
                admins = list(
                    User.objects.filter(role__role_name="Admin").values_list("id", flat=True)
                )
                recipients = [str(aid) for aid in admins]

                # amount_due = total sale amount; amount_payed = what was actually paid
                amount_due = str(instance.sale.total_sale_amount)
                amount_payed = str(instance.amount_paid)
                company_name = instance.sale.shipment.country_origin  # closest to company

                actor_id = str(self.request.user.id)

                trigger_notification(
                    workflow_key="payment_completed",
                    recipients=recipients,
                    actor=actor_id,
                    data={
                        "company_name": company_name,
                        "user": {
                            "name": instance.entered_by.get_full_name() or instance.entered_by.username,
                        },
                        "amount_payed": amount_payed,
                        "amount_due": amount_due,
                        "buyer_name": instance.buyer_name,
                    },
                )
            except Exception as e:
                print(f"Failed to trigger payment_completed Knock notification: {e}")
