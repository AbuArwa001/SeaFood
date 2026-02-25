from rest_framework import permissions, viewsets
from supplierpurchases.models import SupplierPurchase
from .serializers import SupplierPurchaseSerializer


from users.permissions import IsMozambiqueAgent, IsOwnerOrAdmin

class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsMozambiqueAgent, IsOwnerOrAdmin]
    search_fields = ['id', 'shipment__id']

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return SupplierPurchase.objects.all()
        return SupplierPurchase.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)
