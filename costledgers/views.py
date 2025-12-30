from rest_framework import viewsets
from .models import CostLedger
from .serializers import CostLedgerSerializer

class CostLedgerViewSet(viewsets.ModelViewSet):
    queryset = CostLedger.objects.all()
    serializer_class = CostLedgerSerializer