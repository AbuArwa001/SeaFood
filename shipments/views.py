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
        serializer.save(entered_by=self.request.user)