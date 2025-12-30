from rest_framework.routers import DefaultRouter
from .views import SupplierPurchaseViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'supplier_purchases', SupplierPurchaseViewSet)
urlpatterns = [
    path('', include(router.urls)),
]