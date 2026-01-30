from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    unit_name = serializers.ReadOnlyField(source='unit.name')

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'category_name',
            'unit',
            'unit_name',
            'description',
            'is_active',
            'created_at',
        )