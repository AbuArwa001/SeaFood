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
    image_urls = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    id = serializers.UUIDField(read_only=True)
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all())
    shipment_details = ShipmentSerializer(source='shipment', read_only=True)
    entered_by = serializers.PrimaryKeyRelatedField(read_only=True)
    kg_purchased = serializers.DecimalField(max_digits=10, decimal_places=2)
    image_urls = serializers.JSONField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SupplierPurchase
        fields = [
            'id',
            'shipment',
            'shipment_details',
            'currency',
            'entered_by',
            'kg_purchased',
            'image_urls',
            'created_at',
        ]

    def to_representation(self, instance):
        from currencies.serializers import CurrencySerializer
        from audit.serializers import UserSimpleSerializer
        representation = super().to_representation(instance)
        if instance.currency:
            representation['currency'] = CurrencySerializer(instance.currency).data
        if instance.entered_by:
            representation['entered_by_details'] = UserSimpleSerializer(instance.entered_by).data
        return representation