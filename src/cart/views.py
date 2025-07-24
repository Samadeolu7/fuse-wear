# cart/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemOutputSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing shopping cart operations.
    
    Requires JWT authentication for all endpoints.
    Include token in Authorization header: `Bearer <your_token>`
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_value_regex = '[0-9]+'  # Only accept digits for id

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)

    @extend_schema(
        summary="Get cart items",
        description="Retrieves all items in the user's cart with detailed product information",
        responses={
            200: CartItemOutputSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        tags=['Cart Operations']
    )
    def list(self, request):
        """
        Get all items in the user's cart.
        
        Returns a list of cart items with complete product details including:
        - Product information (name, price, description)
        - Selected options (color, size)
        - Current stock levels
        - Images and other metadata
        """
        cart = self.get_queryset().first()
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add item to cart",
        description="Add a new item to the cart with optional color and size selection",
        request=CartItemSerializer,
        responses={
            201: CartItemOutputSerializer,
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Duplicate Item",
                        value={"message": "This item with the same color/size combination already exists in your cart", "error": "duplicate_item"}
                    ),
                    OpenApiExample(
                        "Product Not Found",
                        value={"product_id": ["Product not found"]}
                    ),
                    OpenApiExample(
                        "Insufficient Stock",
                        value={"quantity": ["Only X items available"]}
                    )
                ]
            ),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        tags=['Cart Operations']
    )
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add a new item to the cart"""
        cart = self.get_queryset().first()
        serializer = CartItemSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Handle duplicate item
            return Response({
                "message": "This item with the same color/size combination already exists in your cart",
                "error": "duplicate_item"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e),
                "error": "server_error"
            }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Update cart item",
        description="Update quantity, color, or size of an existing cart item",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="ID of the cart item to update"
            ),
        ],
        request=CartItemSerializer,
        responses={
            200: CartItemOutputSerializer,
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Invalid Quantity",
                        value={"quantity": ["Only X items available"]}
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Not Found",
                examples=[
                    OpenApiExample(
                        "Item Not Found",
                        value={"message": "Item not found in cart", "error": "item_not_found"}
                    )
                ]
            ),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        tags=['Cart Operations']
    )
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update an existing cart item's quantity, color, or size"""
        cart = self.get_queryset().first()
        try:
            item = cart.items.get(id=request.data.get('id'))
            serializer = CartItemSerializer(item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({
                "message": "Item not found in cart",
                "error": "item_not_found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message": str(e),
                "error": "server_error"
            }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Remove item from cart",
        description="Remove a specific item from the cart",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="ID of the cart item to remove",
                required=True
            ),
        ],
        responses={
            204: OpenApiResponse(description="Item successfully removed"),
            404: OpenApiResponse(
                description="Not Found",
                examples=[
                    OpenApiExample(
                        "Item Not Found",
                        value={"message": "Item not found in cart", "error": "item_not_found"}
                    )
                ]
            ),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        tags=['Cart Operations']
    )
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove a specific item from the cart"""
        cart = self.get_queryset().first()
        try:
            item = cart.items.get(id=request.data.get('id'))
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({
                "message": "Item not found in cart",
                "error": "item_not_found"
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Clear cart",
        description="Remove all items from the cart",
        responses={
            204: OpenApiResponse(description="Cart successfully cleared"),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        tags=['Cart Operations']
    )
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Remove all items from the cart"""
        cart = self.get_queryset().first()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)