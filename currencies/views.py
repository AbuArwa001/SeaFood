from django.shortcuts import render

from rest_framework import viewsets
from .models import Currency
from .serializers import CurrencySerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing currency instances.
    """
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    ordering_fields = ['code', 'name', 'symbol']
    ordering = ['code']
