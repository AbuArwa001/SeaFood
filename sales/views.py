from django.shortcuts import render
from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer

from users.permissions import IsSalesAgent, IsOwnerOrAdmin

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [IsSalesAgent, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return Sale.objects.all()
        return Sale.objects.filter(entered_by=user)