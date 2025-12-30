from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing payment instances.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
