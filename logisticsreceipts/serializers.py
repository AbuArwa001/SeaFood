from rest_framework import serializers
from .models import LogisticsReceipt
from shipments.serializers import ShipmentSerializer

class LogisticsReceiptSerializer(serializers.ModelSerializer):
    """
    Docstring for LogisticsReceiptSerializer
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(
        models.Shipment,
        on_delete=models.CASCADE,
        related_name="logistics_receipts"
    )
    entered_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="logistics_receipts"
    )
    net_received_kg = models.DecimalField(max_digits=10, decimal_places=2)
    transport_loss_kg = models.DecimalField(max_digits=10, decimal_places=2)
    freezing_loss_kg = models.DecimalField(max_digits=10, decimal_places=2)
    facility_location = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    """
    shipment_details = ShipmentSerializer(source='shipment', read_only=True)
    entered_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LogisticsReceipt
        fields = [
            'id',
            'shipment',
            'shipment_details',
            'entered_by',
            'net_received_kg',
            'transport_loss_kg',
            'freezing_loss_kg',
            'facility_location',
            'notes',
            'created_at',
        ]