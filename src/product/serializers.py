from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'slug', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'media_type', 'alt_text', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price',
            'sales_count', 'views_count', 'trending_score',
            'aggregated_order_info', 'current_stock', 'is_launch',
            'release_date', 'created_at', 'updated_at',
            'images', 'category', 'category_id'
        )
        read_only_fields = ('id', 'sales_count', 'trending_score', 'created_at', 'updated_at')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value