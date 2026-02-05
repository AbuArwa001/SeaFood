from django.urls import path, include
from rest_framework import routers
from .views import CostLedgerViewSet

router = routers.DefaultRouter()
router.register(r'costledgers', CostLedgerViewSet, basename='costledger')
urlpatterns = router.urls