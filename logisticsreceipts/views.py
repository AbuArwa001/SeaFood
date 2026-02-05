from rest_framework import permissions, viewsets
from .models import LogisticsReceipt
from .serializers import LogisticsReceiptSerializer

from users.permissions import IsLogisticsAgent, IsOwnerOrAdmin

class LogisticsReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = LogisticsReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, IsLogisticsAgent, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return LogisticsReceipt.objects.all()
        return LogisticsReceipt.objects.filter(entered_by=user)