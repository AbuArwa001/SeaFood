from rest_framework import viewsets
from .models import ProductCategory
from .serializers import ProductCategorySerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product category instances.
    """
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    pagination_class = None