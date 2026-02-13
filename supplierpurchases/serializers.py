from rest_framework import serializers
from shipments.models import Shipment
from .models import SupplierPurchase
from shipments.serializers import ShipmentSerializer

class SupplierPurchaseSerializer(serializers.ModelSerializer):
    """
    Docstring for SupplierPurchaseSerializer
        shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="supplier_purchases"
    )
    entered_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="supplier_purchases"
    )
    kg_purchased = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    id = serializers.UUIDField(read_only=True)
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all())
    shipment_details = ShipmentSerializer(source='shipment', read_only=True)
    entered_by = serializers.PrimaryKeyRelatedField(queryset=SupplierPurchase.objects.all())
    kg_purchased = serializers.DecimalField(max_digits=10, decimal_places=2)
    image_url = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SupplierPurchase
        fields = [
            'id',
            'shipment',
            'shipment_details',
            'entered_by',
            'kg_purchased',
            'image_url',
            'created_at',
        ]