from rest_framework import serializers
from .models import Review
from product.serializers import ProductSerializer
from user.serializers import CustomUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    # Represent the related product and user
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductSerializer.Meta.model.objects.all(), source='product', write_only=True
    )
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'product', 'product_id', 'parent',
            'user', 'rating', 'comment', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'user', 'product')
