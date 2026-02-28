from rest_framework import serializers
from .models import Shipment, ShipmentItem
from products.models import Product
from products.serializers import ProductSerializer

from django.db import transaction

# Knock trigger
from notifications.knock_client import trigger_notification
from users.models import User
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
    currency_symbol = serializers.ReadOnlyField(source='currency.symbol')

    class Meta:
        model = Shipment
        fields = [
            'id',
            'currency',
            'currency_code',
            'currency_symbol',
            'country_origin',
            'status',
            'estimated_transit_days',
            'actual_arrival_date',
            'created_at',
            'items',
        ]

    def to_representation(self, instance):
        from currencies.serializers import CurrencySerializer
        representation = super().to_representation(instance)
        if instance.currency:
            representation['currency'] = CurrencySerializer(instance.currency).data
        return representation

    def create(self, validated_data):
        # Extract the items data from the shipment data
        items_data = validated_data.pop('items')
        
        # Either everything saves or nothing does
        with transaction.atomic():
            shipment = Shipment.objects.create(**validated_data)
            
            for item_data in items_data:
                ShipmentItem.objects.create(shipment=shipment, **item_data)
        
        try:
            # Trigger Knock notification to Admins for newly created shipment
            admins = list(User.objects.filter(role__role_name="Admin").values_list('id', flat=True))
            recipients = [str(aid) for aid in admins]
            short_id = str(shipment.id)[:8].upper()
            trigger_notification(
                workflow_key="shipment_created",
                recipients=recipients,
                data={
                    "shipment_id": short_id,
                    "country_origin": shipment.country_origin,
                }
            )
        except Exception as e:
            print(f"Failed to trigger Knock shipment_created: {e}")
        
        return shipment

