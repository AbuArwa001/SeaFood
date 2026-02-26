
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

    @staticmethod
    def get_effective_rate(from_curr, to_curr, date=None):
        """
        Retrieves the latest exchange rate for a pair and applies any active margin.
        Handles both direct and inverse lookups.
        """
        if date is None:
            date = timezone.now().date()
        
        from decimal import Decimal
        from django.utils import timezone

        # 1. Try Direct Rate
        rate_obj = ExchangeRate.objects.filter(
            from_currency=from_curr,
            to_currency=to_curr,
            rate_date__lte=date
        ).order_by('-rate_date').first()

        effective_rate = None
        if rate_obj:
            effective_rate = rate_obj.rate
        else:
            # 2. Try Inverse Rate
            inverse_obj = ExchangeRate.objects.filter(
                from_currency=to_curr,
                to_currency=from_curr,
                rate_date__lte=date
            ).order_by('-rate_date').first()
            
            if inverse_obj:
                effective_rate = Decimal("1.0") / inverse_obj.rate

        if effective_rate is None:
            return None

        # 3. Apply Margin if exists
        margin_obj = CurrencyMargin.objects.filter(
            from_currency=from_curr,
            to_currency=to_curr,
            is_active=True
        ).first()

        if margin_obj:
            # Formula: rate * (1 + margin_percentage / 100)
            # We use addition for margin because typically margins in this context 
            # are markups over the base market rate.
            effective_rate = effective_rate * (Decimal("1.0") + (margin_obj.margin_percentage / Decimal("100.0")))

        return effective_rate

    def __str__(self):
        return f"{self.from_currency} → {self.to_currency} @ {self.rate}"


class CurrencyMargin(models.Model):
    """
    Stores margin/markup percentages for currency pairs.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="margins_from"
    )
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="margins_to"
    )
    margin_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        help_text="Percentage markup to apply (e.g., 2.00 for 2%)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("from_currency", "to_currency")

    def __str__(self):
        return f"Margin {self.from_currency}→{self.to_currency}: {self.margin_percentage}%"

