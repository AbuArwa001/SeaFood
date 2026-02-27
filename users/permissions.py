from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allocates permissions to Admin users only.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user.role, 'role_name', None) == "Admin"

class IsAgent(permissions.BasePermission):
    """
    Allows access to any Agent role.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        agent_roles = [
            "Mozambique Agent", 
            "Logistics Agent", 
            "Sales Agent", 
            "Finance Agent",
            "Admin"
        ]
        return getattr(request.user.role, 'role_name', None) in agent_roles

class IsMozambiqueAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user.role, 'role_name', None) in ["Mozambique Agent", "Admin"]

class IsLogisticsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user.role, 'role_name', None) in ["Logistics Agent", "Admin"]

class IsSalesAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user.role, 'role_name', None) in ["Sales Agent", "Admin"]

class IsFinanceAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user.role, 'role_name', None) in ["Finance Agent", "Admin"]

class IsViewer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user.role, 'role_name', None) in ["Viewer", "Admin", "Finance Agent", "Sales Agent", "Logistics Agent", "Mozambique Agent"]

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit.
    Read-only allowed for other agents if necessary, but edit restricted.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin can do anything
        if getattr(request.user.role, 'role_name', None) == "Admin":
            return True

        # Read permissions are allowed to any agent for visibility
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only to owner
        if hasattr(obj, 'entered_by'):
             return obj.entered_by == request.user
        
        return False

class CanCreateUser(IsAdmin):
    """
    Alias for IsAdmin for clarity in User creation context.
    """
    pass