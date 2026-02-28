from rest_framework import serializers
from .models import ExchangeRate, Currency, CurrencyMargin

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']

class CurrencyMarginSerializer(serializers.ModelSerializer):
    from_currency_detail = CurrencySerializer(source='from_currency', read_only=True)
    to_currency_detail = CurrencySerializer(source='to_currency', read_only=True)

    class Meta:
        model = CurrencyMargin
        fields = [
            'id',
            'from_currency',
            'to_currency',
            'from_currency_detail',
            'to_currency_detail',
            'margin_percentage',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # For backward compatibility, return objects for these fields in the response
        representation['from_currency'] = CurrencySerializer(instance.from_currency).data
        representation['to_currency'] = CurrencySerializer(instance.to_currency).data
        return representation

class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency_detail = CurrencySerializer(source='from_currency', read_only=True)
    to_currency_detail = CurrencySerializer(source='to_currency', read_only=True)
    
    from_curr = serializers.CharField(source='from_currency.code', read_only=True)
    to_curr = serializers.CharField(source='to_currency.code', read_only=True)

    class Meta:
        model = ExchangeRate
        fields = [
            'id',
            'from_currency',
            'to_currency',
            'from_currency_detail',
            'to_currency_detail',
            'rate',
            'rate_date',
            'from_curr',
            'to_curr',
            'created_at',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # For backward compatibility, return objects for these fields in the response
        representation['from_currency'] = CurrencySerializer(instance.from_currency).data
        representation['to_currency'] = CurrencySerializer(instance.to_currency).data
        return representation