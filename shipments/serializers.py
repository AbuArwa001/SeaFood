from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id',
            # 'tracking_number',
            'country_origin',
            'product_name',
            # 'weight',
            'status',
            'created_at',
            # 'delivery_date'
        ]

