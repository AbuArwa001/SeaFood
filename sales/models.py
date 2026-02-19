from decimal import Decimal
from django.db import models
from django.utils import timezone
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
        # 1. Use the current date if the sale is new
        reference_date = self.created_at.date() if self.created_at else timezone.now().date()
        
        shipment_currency = self.shipment.currency

        if self.currency != shipment_currency:
            # 2. Look up the rate (Direct)
            rate_obj = ExchangeRate.objects.filter(
                from_currency=self.currency,
                to_currency=shipment_currency,
                rate_date__lte=reference_date
            ).first() 

            if rate_obj:
                self.exchange_rate_used = rate_obj.rate
            else:
                # 3. Look up the rate (Inverse)
                inverse_rate_obj = ExchangeRate.objects.filter(
                    from_currency=shipment_currency,
                    to_currency=self.currency,
                    rate_date__lte=reference_date
                ).first()

                if not inverse_rate_obj:
                    raise ValueError(f"No exchange rate found for {self.currency} to {shipment_currency} (or inverse) on {reference_date}")
                
                # Inverse rate: if 1 USD = 2500 TZS, then 1 TZS = 1/2500 USD
                self.exchange_rate_used = Decimal("1.0") / inverse_rate_obj.rate

            # 4. Calculate based on your actual field names (quantity * price)
            self.total_sale_amount = self.quantity_sold * self.selling_price
            self.converted_amount = self.total_sale_amount * self.exchange_rate_used
        else:
            self.exchange_rate_used = Decimal("1.0")
            self.total_sale_amount = self.quantity_sold * self.selling_price
            self.converted_amount = self.total_sale_amount

        super().save(*args, **kwargs)