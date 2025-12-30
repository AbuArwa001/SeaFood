from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'shipments', ShipmentViewSet)
urlpatterns = [
    path('', include(router.urls)),
]