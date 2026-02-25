from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ['name', 'category__name', 'unit__description']
