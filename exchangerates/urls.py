from rest_framework.routers import DefaultRouter
from .views import ExchangeRateViewSet, CurrencyMarginViewSet
router = DefaultRouter()
router.register(r'exchange-rates', ExchangeRateViewSet, basename='exchange-rate')
router.register(r'currency-margins', CurrencyMarginViewSet, basename='currency-margin')
urlpatterns = router.urls
