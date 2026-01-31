from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from .models import User, Role


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
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'role_name',
            'full_name',
            'location',
        ]

    def validate_role(self, value):
        """
        Ensure that only Admins can create users with the 'Admin' role.
        """
        request = self.context.get('request')
        if not request:
            return value
        print( f"WHO IS THIS {type(request.user)}",request.user)
        if isinstance(request.user, AnonymousUser):
            print("Anonymous user trying to assign role")
            if value.role_name == "Admin":
                raise serializers.ValidationError("Only an Admin can assign the Admin role.")
        # Check if the role being assigned is "Admin"
        if value.role_name == "Admin" and getattr(request.user.role, 'role_name', None) != "Admin":
            raise serializers.ValidationError("Only an Admin can assign the Admin role.")
        
        # Otherwise it's fine (anyone can assign "User" role)
        return value

class RoleSerializer(serializers.ModelSerializer):
    """
    Docstring for RoleSerializer
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles"
    )
    """
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Role
        fields = [
            'id',
            'role_name',
            'permissions',
        ]