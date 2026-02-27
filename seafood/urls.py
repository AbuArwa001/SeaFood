from django.contrib import admin
from django.urls import path, include
from seafood import root_app
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_v1_patterns = [
    path('', root_app.home, name=''),
    path('', include('users.urls')),
    path('', include('shipments.urls')),
    path('', include('logisticsreceipts.urls')),
    path('', include('supplierpurchases.urls')),
    path('', include('sales.urls')),
    path('', include('costledgers.urls')),
    path('', include('currencies.urls')),
    path('', include('payments.urls')),
    path('', include('exchangerates.urls')),
    path('', include('productcategories.urls')),
    path('', include('unitofmeasures.urls')),
    path('', include('products.urls')),
    path('', include('notifications.urls')),
    path('audit/', include('audit.urls')),
    path('', include('configuration.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(api_v1_patterns)),
]