from rest_framework import permissions, viewsets
from .models import Sale
from .serializers import SaleSerializer

from users.permissions import IsSalesAgent, IsOwnerOrAdmin

from rest_framework.exceptions import ValidationError

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalesAgent, IsOwnerOrAdmin]
    search_fields = ['id', 'shipment__id']

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return Sale.objects.all()
        return Sale.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        try:
            instance = serializer.save(entered_by=self.request.user)
            
            # If actor is NOT an Admin, notify Admins/Agents of the activity
            user = self.request.user
            if user.role.role_name != "Admin":
                try:
                    from notifications.knock_client import trigger_notification
                    from notifications.knock_recipients import get_role_recipients
                    
                    # Notify Admins and Agents
                    recipients = get_role_recipients()
                    actor_payload = {
                        "id": str(user.id),
                        "email": user.email,
                        "name": user.full_name or user.username
                    }
                    actor_name = user.full_name or user.email
                    
                    # Construct items list from shipment items
                    try:
                        shipment_items = instance.shipment.items.select_related('product').all()
                        items_list = ", ".join([f"{item.product.name} ({item.quantity})" for item in shipment_items])
                    except:
                        items_list = "N/A"

                    trigger_notification(
                        workflow_key="sale_created",
                        recipients=recipients,
                        actor=actor_payload,
                        data={
                            "total_price": f"{instance.total_sale_amount} {instance.currency.code if instance.currency else ''}",
                            "items_list": items_list,
                            "sale_id": str(instance.id),
                            "amount": str(instance.total_sale_amount),
                            "kg_sold": str(instance.kg_sold),
                            "actor_name": actor_name,
                            "currency": instance.currency.code if instance.currency else "N/A",
                        },
                    )
                except Exception as e:
                    print(f"Failed to trigger sale_created Knock notification: {e}")

        except ValueError as e:
            raise ValidationError(str(e))