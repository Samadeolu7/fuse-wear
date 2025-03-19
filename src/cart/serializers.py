from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    # Include product details as nested representation
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity', 'added_at', 'subtotal')
        read_only_fields = ('id', 'added_at', 'subtotal')

    def get_subtotal(self, obj):
        return obj.get_subtotal()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'updated_at', 'meta_data', 'items', 'total')
        read_only_fields = ('id', 'created_at', 'updated_at', 'total', 'user')

    def get_total(self, obj):
        return obj.get_total()
