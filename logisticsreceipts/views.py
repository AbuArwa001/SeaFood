from rest_framework import permissions, viewsets
from .models import LogisticsReceipt
from .serializers import LogisticsReceiptSerializer

from users.permissions import IsLogisticsAgent, IsOwnerOrAdmin

class LogisticsReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = LogisticsReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, IsLogisticsAgent, IsOwnerOrAdmin]
    search_fields = ['facility_location', 'notes']

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return LogisticsReceipt.objects.all()
        return LogisticsReceipt.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        instance = serializer.save(entered_by=self.request.user)
        
        # If actor is NOT an Admin, notify Admins/Agents of the activity
        user = self.request.user
        if user.role.role_name != "Admin":
            try:
                from notifications.knock_client import trigger_notification
                from notifications.knock_recipients import get_role_recipients
                
                # Notify Admins and Agents
                recipients = get_role_recipients()
                actor_id = str(user.id)
                actor_name = user.full_name or user.email
                
                trigger_notification(
                    workflow_key="shipment_received",
                    recipients=recipients,
                    actor=actor_id,
                    data={
                        "order_id": str(instance.shipment.id)[:8].upper() if instance.shipment else "N/A",
                        "shipment_id": str(instance.shipment.id)[:8].upper() if instance.shipment else "N/A",
                        "net_received_kg": str(instance.net_received_kg),
                        "facility_location": instance.facility_location,
                        "actor_name": actor_name,
                    },
                )
            except Exception as e:
                print(f"Failed to trigger shipment_received Knock notification: {e}")