from rest_framework import serializers
from .models import Shipment, ShipmentItem
from products.models import Product
from products.serializers import ProductSerializer

from django.db import transaction

class ShipmentItemSerializer(serializers.ModelSerializer):
    # This allows you to see the product details when reading, 
    # but only requires the product ID when writing.
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = ShipmentItem
        fields = [
            'id', 
            'product', 
            'product_details', 
            'quantity', 
            'price_at_shipping'
        ]
        extra_kwargs = {
            'product': {'write_only': True}
        }

class ShipmentSerializer(serializers.ModelSerializer):
    items = ShipmentItemSerializer(many=True)
    currency_code = serializers.ReadOnlyField(source='currency.code')

    class Meta:
        model = Shipment
        fields = [
            'id',
            'currency',
            'currency_code',
            'country_origin',
            'status',
            'created_at',
            'items',
        ]

    def create(self, validated_data):
        # Extract the items data from the shipment data
        items_data = validated_data.pop('items')
        
        # Either everything saves or nothing does
        with transaction.atomic():
            shipment = Shipment.objects.create(**validated_data)
            
            for item_data in items_data:
                ShipmentItem.objects.create(shipment=shipment, **item_data)
        
        return shipment

