from django.db import models
from currencies.models import Currency
from shipments.models import Shipment
from users.models import User
import uuid

# --------------------
# Sales
# --------------------
class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="sales"
    )
    entered_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sales"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="sales"
    )
    kg_sold = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_sale_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.total_sale_amount}"