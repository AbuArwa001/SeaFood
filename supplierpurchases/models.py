from django.db import models
from shipments.models import Shipment
from users.models import User
import uuid

# --------------------
# Supplier Purchases
# --------------------
class SupplierPurchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def __str__(self):
        return f"{self.kg_purchased}kg purchased"


