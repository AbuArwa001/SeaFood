from rest_framework import routers
from .views import SystemParameterViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'system-parameters', SystemParameterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
