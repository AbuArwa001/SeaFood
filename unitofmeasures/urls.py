from rest_framework.routers import DefaultRouter
from .views import UnitOfMeasureViewSet
router = DefaultRouter()
router.register(r'unitofmeasures', UnitOfMeasureViewSet, basename='unitofmeasure')
urlpatterns = router.urls