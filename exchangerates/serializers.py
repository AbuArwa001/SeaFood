from rest_framework import serializers
from .models import ExchangeRate
from currencies.models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'code',
            'name',
            'symbol',
        ]

class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency = CurrencySerializer(read_only=True)
    from_curr = serializers.CharField(source='from_currency.code', read_only=True)
    to_curr = serializers.CharField(source='to_currency.code', read_only=True)
    to_currency = CurrencySerializer(read_only=True)
    class Meta:
        model = ExchangeRate
        fields = [
            'id',
            'from_currency',
            'to_currency',
            'rate',
            'rate_date',
            'from_curr',
            'to_curr',
            'created_at',
        ]