from rest_framework import routers
from .views import (
    RoleViewSet, UserViewSet, PermissionViewSet,
    PasswordResetRequestView, PasswordResetConfirmView
)
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
