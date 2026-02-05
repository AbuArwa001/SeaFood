from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allocates permissions to Admin users only.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.role_name == "Admin"

class IsAgent(permissions.BasePermission):
    """
    Base permission for any Agent role.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # List of all agent roles
        agent_roles = [
            "Mozambique Agent", 
            "Logistics Agent", 
            "Sales Agent", 
            "Finance Agent"
        ]
        return request.user.role.role_name in agent_roles or request.user.role.role_name == "Admin"

class IsMozambiqueAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.role_name == "Mozambique Agent" or request.user.role.role_name == "Admin"

class IsLogisticsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.role_name == "Logistics Agent" or request.user.role.role_name == "Admin"

class IsSalesAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.role_name == "Sales Agent" or request.user.role.role_name == "Admin"

class IsFinanceAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.role_name == "Finance Agent" or request.user.role.role_name == "Admin"

class IsViewer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.role_name == "Viewer" or request.user.role.role_name == "Admin"

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `entered_by` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # But wait, requirement says "Users can only view and edit data they created unless Admin"
        # So we should probably restrict Read too if it's not the owner?
        # The requirement says "Users can only view and edit data they created".
        # So we need to enforce this in the View's QuerySet AND here for object access.
        
        # Admin can do anything
        if request.user.role.role_name == "Admin":
            return True

        if hasattr(obj, 'entered_by'):
             return obj.entered_by == request.user
        
        return False