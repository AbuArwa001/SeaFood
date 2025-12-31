from rest_framework import viewsets
from .models import UnitOfMeasure
from .serializers import UnitOfMeasureSerializer


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing unit of measure instances.
    """
    serializer_class = UnitOfMeasureSerializer
    queryset = UnitOfMeasure.objects.all()