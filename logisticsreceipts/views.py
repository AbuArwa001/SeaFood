from django.shortcuts import render
from rest_framework import viewsets
from .models import LogisticsReceipt
from .serializers import LogisticsReceiptSerializer

class LogisticsReceiptViewSet(viewsets.ModelViewSet):
    queryset = LogisticsReceipt.objects.all()
    serializer_class = LogisticsReceiptSerializer