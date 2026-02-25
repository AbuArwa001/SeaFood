from rest_framework import viewsets, permissions
from .models import CostLedger
from .serializers import CostLedgerSerializer

from users.permissions import IsLogisticsAgent, IsFinanceAgent, IsAdmin, IsOwnerOrAdmin

class CostLedgerViewSet(viewsets.ModelViewSet):
    serializer_class = CostLedgerSerializer
    # Complex permission: Logistics OR Finance OR Admin
    # And specifically enforce OwnerOrAdmin for object access
    # We can use a custom permission class or bitwise operators if Permission class supports it.
    # But standard DRF permissions are ANDed by default in the list? No, they are checked sequentially.
    # Wait, DRF list is AND. base_permission objects are AND?
    # Actually, we can just define a combined permission or use 'OR' logic in a custom class.
    # But let's use the property that if any permission class returns False, access is denied.
    # So we need one class that says "Is (Logistics OR Finance OR Admin)".
    # My existing classes are single role checks.
    # Let's import the specific ones and rely on a custom check here or just use IsOwnerOrAdmin + logic in get_queryset?
    # Permission classes usually check "Has access to this specific view".
    # I'll create a composite permission inline or just use `IsAuthenticated` (default) AND `IsOwnerOrAdmin` AND filter queryset heavily.
    # Use IsOwnerOrAdmin is good. But we want to block Mozambique/Sales completely.
    # Create a local permission or use the ones I made.
    
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin] 
    search_fields = ['cost_category', 'other_category']

    def get_queryset(self):
        user = self.request.user
        # Block unauthorized roles completely (Validation Layer 1)
        allowed_roles = ["Admin", "Logistics Agent", "Finance Agent"]
        if user.role.role_name not in allowed_roles:
            return CostLedger.objects.none()

        if user.role.role_name == "Admin":
            return CostLedger.objects.all()
        
        # Logistics and Finance see only their own entries
        return CostLedger.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)