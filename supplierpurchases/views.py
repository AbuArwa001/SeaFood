from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from supplierpurchases.models import SupplierPurchase
from .serializers import SupplierPurchaseSerializer


class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    queryset = SupplierPurchase.objects.all()
    serializer_class = SupplierPurchaseSerializer
