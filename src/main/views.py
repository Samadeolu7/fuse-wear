from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    summary="Landing Page Data",
    description=(
        "Returns data for the landing page, including:\n"
        "- All categories\n"
        "- 8 bestsellers\n"
        "- 8 trending products\n"
        "- 8 new arrivals"
    ),
    responses={
        200: OpenApiResponse(
            response={
                "categories": CategorySerializer(many=True),
                "bestsellers": ProductSerializer(many=True),
                "trending": ProductSerializer(many=True),
                "new_arrivals": ProductSerializer(many=True),
            },
            description="Landing page data successfully retrieved.",
        ),
        404: OpenApiResponse(description="Data not found."),
    },
)
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