# --------------------
# Logistics Receipts
# --------------------
import uuid
from shipments.models import Shipment
from django.db import models
from users.models import User


class LogisticsReceipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(
        Shipment,
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

    def __str__(self):
        return f"Receipt {self.net_received_kg}kg"