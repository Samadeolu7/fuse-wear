# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product

class CartItemOutputSerializer(serializers.Serializer):
    """
    Serializer for cart item output representation.
    """
    id = serializers.IntegerField(help_text="Product ID")
    cartItemId = serializers.IntegerField(help_text="Cart item ID for frontend use")
    name = serializers.CharField(help_text="Product name")
    price = serializers.CharField(help_text="Product price as string")
    description = serializers.CharField(help_text="Product description")
    category = serializers.CharField(help_text="Product category name")
    tags = serializers.ListField(
        help_text="List of product tags",
        child=serializers.DictField()
    )
    images = serializers.ListField(
        help_text="List of product images",
        child=serializers.DictField()
    )
    quantity = serializers.IntegerField(help_text="Quantity in cart")
    selectedColor = serializers.CharField(help_text="Selected color variant")
    selectedSize = serializers.CharField(help_text="Selected size variant")
    current_stock = serializers.IntegerField(help_text="Current available stock")
    created_at = serializers.DateTimeField(help_text="Product creation timestamp")
    updated_at = serializers.DateTimeField(help_text="Product last update timestamp")

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for cart items with complete product information.
    """
    product_id = serializers.IntegerField(
        write_only=True,
        help_text="ID of the product to add to cart"
    )
    quantity = serializers.IntegerField(
        help_text="Quantity of the item",
        min_value=1
    )
    selected_color = serializers.CharField(
        help_text="Selected color variant",
        required=False,
        allow_blank=True
    )
    selected_size = serializers.CharField(
        help_text="Selected size variant",
        required=False,
        allow_blank=True
    )
    
    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity', 'selected_color', 'selected_size')

    def validate(self, data):
        """
        Validate the cart item data.
        
        Args:
            data (dict): The data to validate containing product_id and quantity
            
        Returns:
            dict: The validated data with the product instance added
            
        Raises:
            ValidationError: If product doesn't exist or quantity exceeds stock
        """
        try:
            product = Product.objects.get(id=data['product_id'])
            if data.get('quantity', 1) > product.current_stock:
                raise serializers.ValidationError({
                    "quantity": f"Only {product.current_stock} items available"
                })
            data['product'] = product
            return data
        except Product.DoesNotExist:
            raise serializers.ValidationError({
                "product_id": "Product not found"
            })

    def to_representation(self, instance):
        """Convert to frontend expected format"""
        product = instance.product
        return {
            "id": instance.id,
            "cartItemId": str(instance.id),
            "name": product.name,
            "price": str(product.price),
            "description": product.description,
            "category": product.category.name if product.category else "",
            "tags": [{"id": t.id, "name": t.name, "value": t.value} for t in product.tags.all()],
            "images": [{
                "id": img.id,
                "image": img.image,
                "media_type": img.media_type,
                "alt_text": img.alt_text,
                "is_primary": img.is_primary
            } for img in product.images.all()],
            "quantity": instance.quantity,
            "selectedColor": instance.selected_color or "",
            "selectedSize": instance.selected_size or "",
            "current_stock": product.current_stock,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat()
        }

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    """
    items = CartItemSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user_id', 'items')
        read_only_fields = ('id', 'user_id')