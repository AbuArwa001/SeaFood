from rest_framework import viewsets, permissions, views, response
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from django.db import connection
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['action', 'user', 'content_type']
    search_fields = ['object_repr', 'details', 'object_id']
    ordering_fields = ['timestamp']

class SystemStatsView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # 1. Database generic stats
        models_to_stats = [
            'shipments.Shipment',
            'sales.Sale',
            'supplierpurchases.SupplierPurchase',
            'logisticsreceipts.LogisticsReceipt',
            'payments.Payment',
            'costledgers.CostLedger'
        ]
        
        counts = {}
        for model_path in models_to_stats:
            try:
                model = apps.get_model(model_path)
                counts[model.__name__] = model.objects.count()
            except:
                counts[model_path] = 0

        # 2. Activity summary (last 24h)
        from django.utils import timezone
        import datetime
        day_ago = timezone.now() - datetime.timedelta(days=1)
        recent_activity_count = ActivityLog.objects.filter(timestamp__gte=day_ago).count()

        # 3. User stats
        from users.models import User
        user_stats = {
            'total': User.objects.count(),
            'active': User.objects.filter(is_active=True).count()
        }

        return response.Response({
            'model_counts': counts,
            'recent_activity_count': recent_activity_count,
            'user_stats': user_stats,
            'database_engine': connection.vendor,
        })
