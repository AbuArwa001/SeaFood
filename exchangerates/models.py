
# =========================
# Exchange Rates
# =========================
from currencies.models import Currency
from django.db import models
from django.core.exceptions import ValidationError
import uuid


class ExchangeRate(models.Model):
    """
    Stores historical exchange rates.
    Rates must NEVER be updated retroactively.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="rates_from"
    )
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="rates_to"
    )

    rate = models.DecimalField(max_digits=12, decimal_places=6)
    rate_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_currency", "to_currency", "rate_date")
        ordering = ["-rate_date"]

    def clean(self):
        if self.from_currency == self.to_currency:
            raise ValidationError("From and To currencies must be different.")

    def __str__(self):
        return f"{self.from_currency} → {self.to_currency} @ {self.rate}"

