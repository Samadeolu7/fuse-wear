from rest_framework import serializers
from .models import Category, Product, ProductImage, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'slug', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'media_type', 'alt_text', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    images_ids = serializers.PrimaryKeyRelatedField(
        queryset=ProductImage.objects.all(), source='images', write_only=True, many=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', write_only=True, many=True
    )
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
            'release_date', 'created_at', 'updated_at', 'images_ids',
            'images', 'category', 'category_id', 'tags', 'tags_ids'
        )
        read_only_fields = ('id', 'sales_count', 'trending_score', 'created_at', 'updated_at', 'images', 'tags')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value