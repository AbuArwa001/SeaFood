from  rest_framework import routers
from .views import LogisticsReceiptViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'logistics-receipts', LogisticsReceiptViewSet, basename='logisticsreceipt')
urlpatterns = [
    path('', include(router.urls)),
]