from rest_framework import serializers
from .models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCategory model.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'name',
            'created_at',
        ]