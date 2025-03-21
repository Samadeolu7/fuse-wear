from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import ProductViewSet, ProductImageViewSet, CategoryViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='product-image')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
