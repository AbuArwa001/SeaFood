from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer


from users.permissions import IsFinanceAgent, IsOwnerOrAdmin

class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing payment instances.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsFinanceAgent, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return Payment.objects.all()
        return Payment.objects.filter(entered_by=user)

