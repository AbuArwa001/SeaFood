from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from supplierpurchases.models import SupplierPurchase
from .serializers import SupplierPurchaseSerializer


from users.permissions import IsMozambiqueAgent, IsOwnerOrAdmin

class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierPurchaseSerializer
    permission_classes = [IsMozambiqueAgent, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return SupplierPurchase.objects.all()
        return SupplierPurchase.objects.filter(entered_by=user)
