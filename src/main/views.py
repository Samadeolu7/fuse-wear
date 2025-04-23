from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.schemas import exclude_schema
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


#define ping

def ping(request):
    """
    Simple ping endpoint to check if the server is running.
    """
    return Response({"message": "pong"}, status=status.HTTP_200_OK)



@api_view(['GET'])
def landing_page(request):
    """
    Returns data for the landing page:
    - All categories
    - 8 bestsellers
    - 8 trending products
    - 8 new arrivals
    """
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
    new_arrivals = Product.objects.filter(release_date__lte=timezone.now()).order_by('-release_date')[:8]
    new_arrivals_serializer = ProductSerializer(new_arrivals, many=True)

    # Combine all data into a single response
    data = {
        "categories": category_serializer.data,
        "bestsellers": bestsellers_serializer.data,
        "trending": trending_serializer.data,
        "new_arrivals": new_arrivals_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)