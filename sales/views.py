from rest_framework import permissions, viewsets
from .models import Sale
from .serializers import SaleSerializer

from users.permissions import IsSalesAgent, IsOwnerOrAdmin

from rest_framework.exceptions import ValidationError

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalesAgent, IsOwnerOrAdmin]
    search_fields = ['sale_number', 'customer_name', 'product__name']

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return Sale.objects.all()
        return Sale.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        try:
            serializer.save(entered_by=self.request.user)
        except ValueError as e:
            raise ValidationError(str(e))