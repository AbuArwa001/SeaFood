import uuid
from django.db import models


class Currency(models.Model):
    """
    ISO 4217 currency model
    Example:
        code: USD
        name: US Dollar
        symbol: $
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3, unique=True)   # ISO 4217
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code