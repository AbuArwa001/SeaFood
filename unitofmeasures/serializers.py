from rest_framework import serializers
from .models import UnitOfMeasure


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    """
    Docstring for UnitOfMeasureSerializer

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    class Meta:
        model = UnitOfMeasure
        fields = (
            'id',
            'code',
            'description',
            'created_at',
        )