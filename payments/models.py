
# --------------------
# Payments
# --------------------
import uuid
from sales.models import Sale
from users.models import User
from django.db import models


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    entered_by = models.ForeignKey(
        models.User,
        on_delete=models.PROTECT,
        related_name="payments"
    )
    buyer_name = models.CharField(max_length=255)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    expected_payment_date = models.DateField()
    actual_payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.amount_paid}"