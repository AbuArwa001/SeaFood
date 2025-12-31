from decimal import Decimal
from django.db import models
from currencies.models import Currency
from exchangerates.models import ExchangeRate
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
    exchange_rate_used = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        null=True,
        blank=True
    )
    converted_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    total_sale_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.total_sale_amount}"
    
    def save(self, *args, **kwargs):
        shipment_currency = self.shipment.currency

        if self.currency != shipment_currency:
            rate = ExchangeRate.objects.filter(
                from_currency=self.currency,
                to_currency=shipment_currency,
                rate_date__lte=self.created_at.date()
            ).order_by("-rate_date").first()

            if not rate:
                raise ValueError("Missing exchange rate")

            self.exchange_rate_used = rate.rate
            self.converted_amount = self.amount * rate.rate
        else:
            self.exchange_rate_used = Decimal("1.0")
            self.converted_amount = self.amount

        super().save(*args, **kwargs)