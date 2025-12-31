from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Docstring for ProductSerializer

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products"
    )

    unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name="products"
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'unit',
            'description',
            'is_active',
            'created_at',
        )