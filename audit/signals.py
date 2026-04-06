from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog

# Import models to track
from shipments.models import Shipment
from sales.models import Sale
from supplierpurchases.models import SupplierPurchase
from logisticsreceipts.models import LogisticsReceipt
from payments.models import Payment
from costledgers.models import CostLedger
from exchangerates.models import ExchangeRate, CurrencyMargin
from users.models import User

MODELS_TO_TRACK = [
    Shipment, Sale, SupplierPurchase, LogisticsReceipt, 
    Payment, CostLedger, ExchangeRate, CurrencyMargin, User
]

def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_activity(instance, action, user=None):
    from .middleware import get_current_user
    
    ct = ContentType.objects.get_for_model(instance)
    
    if not user:
        # 1. ThreadLocal user (most precise)
        thread_user = get_current_user()
        if thread_user:
            user = thread_user
        # 2. Fallback to entered_by if available
        elif hasattr(instance, 'entered_by'):
            user = instance.entered_by

    ActivityLog.objects.create(
        user=user,
        action=action,
        content_type=ct,
        object_id=str(instance.pk),
        object_repr=str(instance),
        details={
            'model': instance.__class__.__name__,
            'app_label': ct.app_label,
            # We could add more field-level changes here if needed
        }
    )

@receiver(post_save)
def track_save(sender, instance, created, **kwargs):
    if sender in MODELS_TO_TRACK:
        action = 'CREATE' if created else 'UPDATE'
        log_activity(instance, action)

@receiver(post_delete)
def track_delete(sender, instance, **kwargs):
    if sender in MODELS_TO_TRACK:
        log_activity(instance, 'DELETE')
