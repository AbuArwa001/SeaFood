from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Docstring for UserSerializer
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users"
    )
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    """
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'full_name',
            'location',
        ]
