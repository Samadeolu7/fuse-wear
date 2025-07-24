from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, generics
from main.serializers import LandingPageSerializer
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


#define ping

def ping(request):
    """
    Simple ping endpoint to check if the server is running.
    """
    return Response({"message": "pong"}, status=status.HTTP_200_OK)



class LandingPageView(generics.GenericAPIView):
    """
    Returns curated data for the landing page including categories and featured products.
    """
    serializer_class = LandingPageSerializer

    @extend_schema(
        summary="Landing Page Data",
        description="Returns curated data for the landing page including categories and featured products",
        responses={
            200: LandingPageSerializer,
            500: OpenApiResponse(description="Server error")
        },
        tags=['Main']
    )
    def get(self, request):
        """
        Returns:
        - All categories
        - 8 bestsellers (most ordered products)
        - 8 trending products (most viewed/carted)
        - 8 new arrivals (recently added products)
        """
        try:
            # Fetch all categories
            categories = Category.objects.all()
            category_serializer = CategorySerializer(categories, many=True)
            
            # Fetch 8 bestsellers
            bestsellers = Product.objects.order_by('-sales_count')[:8]
            bestsellers_serializer = ProductSerializer(bestsellers, many=True)
            
            # Fetch 8 trending products
            trending = Product.objects.order_by('-trending_score')[:8]
            trending_serializer = ProductSerializer(trending, many=True)
            
            # Fetch 8 new arrivals
            new_arrivals = Product.objects.order_by('-created_at')[:8]
            new_arrivals_serializer = ProductSerializer(new_arrivals, many=True)
            
            data = {
                "categories": category_serializer.data,
                "bestsellers": bestsellers_serializer.data,
                "trending": trending_serializer.data,
                "new_arrivals": new_arrivals_serializer.data
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": "Failed to fetch landing page data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )