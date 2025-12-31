from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet
router = DefaultRouter()
router.register(r'productcategories', ProductCategoryViewSet, basename='productcategory')
urlpatterns = router.urls
