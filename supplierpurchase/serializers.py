from rest_framework import serializers
from .models import SupplierPurchase

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

    class Meta:
        model = SupplierPurchase
        fields = [
            'id',
            'shipment',
            'entered_by',
            'kg_purchased',
            'image_url',
            'created_at',
        ]