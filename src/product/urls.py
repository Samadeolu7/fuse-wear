from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import ProductViewSet, ProductImageViewSet, CategoryViewSet, TagViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='product-image')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
