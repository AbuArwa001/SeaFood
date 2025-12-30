from django.db import models
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
    currncy = models.CharField(max_length=10, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cost_category} - {self.amount}"