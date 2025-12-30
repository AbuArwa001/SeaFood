from rest_framework import serializers
from .models import Sale
from users.serializers import UserSerializer
from shipments.serializers import ShipmentSerializer

class SaleSerializer(serializers.ModelSerializer):
    entered_by = UserSerializer(read_only=True)
    shipment = ShipmentSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id',
            'shipment',
            'entered_by',
            'kg_sold',
            'quantity_sold',
            'selling_price',
            'converted_amount',
            'total_sale_amount',
            'created_at',
        ]