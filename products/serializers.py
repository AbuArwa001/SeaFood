from rest_framework import serializers
from .models import Product
from productcategories.serializers import ProductCategorySerializer
from unitofmeasures.serializers import UnitOfMeasureSerializer

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    unit_name = serializers.ReadOnlyField(source='unit.code')

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ProductCategorySerializer(instance.category).data
        representation['unit'] = UnitOfMeasureSerializer(instance.unit).data
        return representation