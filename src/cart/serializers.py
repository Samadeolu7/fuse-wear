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

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity', 'added_at')

    def create(self, validated_data):
        # Get the authenticated user's cart
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the product already exists in the cart
        product = validated_data['product']
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_item:
            self.instance = existing_item
            self.instance.quantity += validated_data['quantity']
            self.instance.save()
            return self.instance

        # Associate the CartItem with the user's cart
        validated_data['cart'] = cart
        return super().create(validated_data)
    
    def validate_quantity(self, value):
        product_id = self.initial_data.get('product_id')
        if product_id:
            try:
                product_instance = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"detail": "Product does not exist."})
    
            if value > product_instance.current_stock:
                raise serializers.ValidationError({"detail": "Not enough stock available."})
        return value

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'updated_at', 'meta_data', 'items', 'total')
        read_only_fields = ('id', 'created_at', 'updated_at', 'total', 'user')

    def get_total(self, obj):
        return obj.get_total()
