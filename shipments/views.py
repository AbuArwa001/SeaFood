from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ShipmentSerializer
from .models import Shipment
from users.permissions import IsAgent, IsOwnerOrAdmin

class ShipmentViewSet(viewsets.ModelViewSet):
    serializer_class = ShipmentSerializer
    permission_classes = [IsAgent, IsOwnerOrAdmin]
    search_fields = ['id', 'country_origin', 'status']

    def get_queryset(self):
        user = self.request.user
        
        # Admin sees everything
        if user.role.role_name == "Admin":
            return Shipment.objects.all()
        
        # Mozambique Agents only see their own entries
        if user.role.role_name == "Mozambique Agent":
            return Shipment.objects.filter(entered_by=user)
            
        # Other agents see everything for now
        return Shipment.objects.all()

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
                actor_payload = {
                    "id": str(user.id),
                    "email": user.email,
                    "name": user.full_name or user.username
                }
                actor_name = user.full_name or user.email
                
                trigger_notification(
                    workflow_key="shipment_created",
                    recipients=recipients,
                    actor=actor_payload,
                    data={
                        "shipment_id": str(instance.id)[:8].upper(),
                        "country_origin": instance.country_origin,
                        "actor_name": actor_name,
                        "status": instance.get_status_display() if hasattr(instance, 'get_status_display') else instance.status,
                    },
                )
            except Exception as e:
                print(f"Failed to trigger shipment_created Knock notification: {e}")