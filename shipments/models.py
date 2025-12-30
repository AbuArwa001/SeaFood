from django.db import models
import uuid

from currencies.models import Currency

# --------------------
# Shipments
# --------------------
class Shipment(models.Model):
    STATUS_CHOICES = (
        ("CREATED", "Created"),
        ("IN_TRANSIT", "In Transit"),
        ("RECEIVED", "Received"),
        ("COMPLETED", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="shipments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    country_origin = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.product_name} ({self.status})"

