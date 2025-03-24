# cart/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    Manages the shopping cart for the authenticated user.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return the authenticated user's cart
        user = self.request.user
        return Cart.objects.filter(user=user)

    @method_decorator(cache_page(30))
    def retrieve(self, request, *args, **kwargs):
        # Cache cart details for 30 seconds
        return super().retrieve(request, *args, **kwargs)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Manages cart items for the authenticated user.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter cart items by the authenticated user's cart
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return CartItem.objects.filter(cart=cart)
