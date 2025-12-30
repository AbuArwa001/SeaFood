from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import SupplierPurchaseSerializer
from users.models import User

class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SupplierPurchaseSerializer
