# cart/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)

    def list(self, request):
        """Get cart with items"""
        cart = self.get_queryset().first()
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
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

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update cart item"""
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

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
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

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = self.get_queryset().first()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)