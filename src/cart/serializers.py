from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    cartItemId = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = (
            'id', 'cartItemId', 'product_id', 'product_details',
            'quantity', 'selected_color', 'selected_size', 'added_at'
        )
        read_only_fields = ('id', 'added_at')

    def get_cartItemId(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_data = data.pop('product_details', {})
        return {
            **product_data,
            'cartItemId': data['cartItemId'],
            'quantity': data['quantity'],
            'selectedColor': data['selected_color'],
            'selectedSize': data['selected_size'],
        }

    def validate(self, data):
        try:
            product = Product.objects.get(id=data['product_id'])
            if data.get('quantity', 1) > product.current_stock:
                raise serializers.ValidationError(
                    f"Only {product.current_stock} items available"
                )
            data['product'] = product
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')