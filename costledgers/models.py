from django.db import models
from currencies.models import Currency
from exchangerates.models import ExchangeRate
from shipments.models import Shipment
from users.models import User
import uuid
# --------------------
# Cost Ledger
# --------------------

class CostLedger(models.Model):
    class CategoryChoices(models.TextChoices):
        """
        Docstring for CategoryChoices
        Common cost categories include:
            Transport
            Freezing
            Cold Storage
            Packing Materials
            Labor
            Commissions
            Export Fees
            Fuel
            Accommodation
            Meals
            Miscellaneous (please specify in notes)
        """
        TRANSPORT = "Transport"
        FREEZING = "Freezing"
        COLD_STORAGE = "Cold Storage"
        PACKING_MATERIALS = "Packing Materials"
        LABOR = "Labor"
        COMMISSIONS = "Commissions"
        EXPORT_FEES = "Export Fees"
        FUEL = "Fuel"
        ACCOMMODATION = "Accommodation"
        MEALS = "Meals"
        MISCELLANEOUS = "Miscellaneous"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="costs"
    )
    entered_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="costs"
    )
    cost_category = models.CharField(
        max_length=100,
        choices=CategoryChoices.choices
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    other_category = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Required if category is Miscellaneous"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='cost_ledgers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
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
    def __str__(self):
        return f"{self.cost_category} - {self.amount}"
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
            self.converted_amount = self.amount

        super().save(*args, **kwargs)