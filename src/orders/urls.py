from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]