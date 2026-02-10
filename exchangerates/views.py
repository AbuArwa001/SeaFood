from rest_framework import viewsets
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from exchangerates.filters import ExchangeRateFilter

class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.order_by('-rate_date')
    serializer_class = ExchangeRateSerializer
    filter_backends= [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExchangeRateFilter
    # filterset_fields = ['from_currency__code', 'to_currency__code', 'rate_date']
    # search_fields = ['from_currency__code', 'to_currency__code']
    # ordering_fields = ['rate_date', 'rate']
    # ordering = ['-rate_date']