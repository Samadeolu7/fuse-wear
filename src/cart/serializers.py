# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity', 'selected_color', 'selected_size')

    def validate(self, data):
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
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items')