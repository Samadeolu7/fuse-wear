from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Exposes endpoints for standard product operations as well as dynamic sections:
    - Bestsellers
    - Trending
    - New Arrivals
    """
    queryset = Product.objects.select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_launch', 'current_stock']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'sales_count', 'release_date']

    @method_decorator(cache_page(60, key_prefix="bestsellers"))
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        bestsellers = Product.objects.order_by('-sales_count')[:10]
        if not bestsellers.exists():
            return Response({"detail": "No bestsellers found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(bestsellers, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60, key_prefix="trending"))
    @action(detail=False, methods=['get'])
    def trending(self, request):
        trending = Product.objects.order_by('-trending_score')[:10]
        if not trending.exists():
            return Response({"detail": "No trending products found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60, key_prefix="new_arrivals"))
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        new_arrivals = Product.objects.filter(release_date__lte=timezone.now()).order_by('-release_date')[:10]
        if not new_arrivals.exists():
            return Response({"detail": "No new arrivals found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(new_arrivals, many=True)
        return Response(serializer.data)