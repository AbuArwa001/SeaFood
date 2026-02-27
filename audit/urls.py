from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityLogViewSet, SystemStatsView

router = DefaultRouter()
router.register(r'logs', ActivityLogViewSet, basename='activity-logs')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', SystemStatsView.as_view(), name='system-stats'),
]
