
from django.db import models
import uuid

from currencies.models import Currency
from products.models import Product

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

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="shipments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    country_origin = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Shipment {self.id} ({self.status})"

class ShipmentItem(models.Model):
    """
    This connects Products to Shipments and tracks how many of 
    each product are in a specific shipment.
    """
    shipment = models.ForeignKey(
        Shipment, 
        on_delete=models.CASCADE, 
        related_name="items"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name="shipment_items"
    )
    quantity = models.PositiveIntegerField()
    # You might also want to snapshot the price at time of shipping
    price_at_shipping = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.shipment.id}"
    
