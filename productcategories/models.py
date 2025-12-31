from django.db import models
import uuid

# =========================
# Product Categories
# =========================
class ProductCategory(models.Model):
    """
    Examples: Fish, Shellfish
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
