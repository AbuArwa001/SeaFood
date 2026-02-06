from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser, Permission
from .models import User, Role

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class RoleSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = [
            'id',
            'role_name',
            'permissions',
        ]

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    # Use nested serializer for read operations to provide permissions
    role = RoleSerializer(read_only=True)
    # Add a write-only field for role assignment during creation/update
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'role_id',
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