from rest_framework import routers
from .views import RoleViewSet, UserViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
