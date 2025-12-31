from django.db import models
import uuid

# =========================
# Units of Measure
# =========================
class UnitOfMeasure(models.Model):
    """
    Examples:
        kg  - Kilograms
        pcs - Pieces
        ctn - Cartons
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code
