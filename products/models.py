import uuid
from django.db import models

from productcategories.models import ProductCategory
from unitofmeasures.models import UnitOfMeasure

# =========================
# Products
# =========================
class Product(models.Model):
    """
    Central product catalog.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products"
    )

    unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name="products"
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name