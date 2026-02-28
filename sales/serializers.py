from rest_framework import serializers
from .models import Sale
from users.serializers import UserSerializer
from shipments.serializers import ShipmentSerializer
from shipments.models import Shipment

class SaleSerializer(serializers.ModelSerializer):
    entered_by = UserSerializer(read_only=True)
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all())
    
    # Calculated fields should be read-only
    total_sale_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    converted_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id',
            'shipment',
            'entered_by',
            'currency',
            'kg_sold',
            'quantity_sold',
            'selling_price',
            'converted_amount',
            'total_sale_amount',
            'created_at',
        ]

    def to_representation(self, instance):
        from currencies.serializers import CurrencySerializer
        representation = super().to_representation(instance)
        if instance.currency:
            representation['currency'] = CurrencySerializer(instance.currency).data
        return representation