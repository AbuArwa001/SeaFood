from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role.role_name == 'Admin')

class CanCreateUser(BasePermission):
    """
    Only allow Admins to create users with the Admin role.
    """
    def has_permission(self, request, view):
        # Only applies to 'create' action
        if view.action != 'create':
            return True
        
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Only Admins can create users with Admin role
        role_name = request.data.get('role_name')
        if role_name == 'Admin' and getattr(request.user.role, 'role_name', None) != 'Admin':
            return False
        return True