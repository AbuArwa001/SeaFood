from rest_framework import serializers
from .models import Payment
from sales.serializers import SaleSerializer

class PaymentSerializer(serializers.ModelSerializer):
    """
    Docstring for PaymentSerializer
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
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="payments"
    )
    buyer_name = models.CharField(max_length=255)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    expected_payment_date = models.DateField()
    actual_payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    """
    sale_details = SaleSerializer(source='sale', read_only=True)
    class Meta:
        model = Payment
        fields = (
            'id',
            'sale',
            'sale_details',
            'entered_by',
            'currency',
            'buyer_name',
            'amount_paid',
            'expected_payment_date',
            'actual_payment_date',
            'created_at',
        )