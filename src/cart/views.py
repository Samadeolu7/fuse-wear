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
        # Return the cart(s) for the logged-in user
        return Cart.objects.filter(user=self.request.user)

    @method_decorator(cache_page(30))
    def retrieve(self, request, *args, **kwargs):
        # Cache cart details for 30 seconds
        return super().retrieve(request, *args, **kwargs)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Manages individual items within a cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return cart items for the authenticated user's cart
        return CartItem.objects.filter(cart__user=self.request.user)
