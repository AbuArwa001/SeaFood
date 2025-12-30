from rest_framework import serializers
from .models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    """
    Docstring for CurrencySerializer
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    """
    class Meta:
        model = Currency
        fields = (
            'id',
            'code',
            'name',
            'symbol',
            'created_at',
        )