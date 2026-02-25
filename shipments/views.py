from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import ShipmentSerializer
from .models import Shipment

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    search_fields = ['shipment_number', 'origin', 'destination', 'vessel_name']