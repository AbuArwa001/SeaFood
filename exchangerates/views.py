from rest_framework import viewsets, permissions
from .models import ExchangeRate, CurrencyMargin
from .serializers import ExchangeRateSerializer, CurrencyMarginSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from exchangerates.filters import ExchangeRateFilter
from users.permissions import IsAdmin, IsFinanceAgent, IsViewer

class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.order_by('-rate_date')
    serializer_class = ExchangeRateSerializer
    filter_backends= [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExchangeRateFilter
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsViewer()]

class CurrencyMarginViewSet(viewsets.ModelViewSet):
    queryset = CurrencyMargin.objects.all()
    serializer_class = CurrencyMarginSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['from_currency', 'to_currency', 'is_active']
    search_fields = ['from_currency__code', 'to_currency__code']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsViewer()]