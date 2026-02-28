from rest_framework import serializers
from shipments.serializers import ShipmentSerializer
from users.serializers import UserSerializer
from shipments.serializers import ShipmentSerializer
from .models import CostLedger


class CostLedgerSerializer(serializers.ModelSerializer):
    """
    Docstring for CostLedgerSerializer
class CostLedger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="costs"
    )
    entered_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="costs"
    )
    cost_category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    """

    # shipment = ShipmentSerializer(read_only=True)
    entered_by = UserSerializer(read_only=True)
    id = serializers.UUIDField(read_only=True)
    converted_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    exchange_rate_used = serializers.DecimalField(max_digits=12, decimal_places=6, read_only=True)

    class Meta:
        model = CostLedger
        fields = [
            'id',
            'shipment',
            'entered_by',
            'cost_category',
            'exchange_rate_used',
            'converted_amount',
            'currency',
            'amount',
            'created_at',
        ]

    def to_representation(self, instance):
        from currencies.serializers import CurrencySerializer
        representation = super().to_representation(instance)
        if instance.currency:
            representation['currency'] = CurrencySerializer(instance.currency).data
        return representation