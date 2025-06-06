from django.urls import path, include

from rest_framework.routers import DefaultRouter
from drf_spectacular.utils import extend_schema

from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]

