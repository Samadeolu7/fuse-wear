from rest_framework import serializers
from .models import Category, Manufacturer, Product, ProductImage, ProductTag, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "slug", "created_at", "updated_at")
        read_only_fields = ("id", "slug", "created_at", "updated_at")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "media_type", "alt_text", "is_primary", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class ProductTagSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source="tag",
        write_only=True
    )
    image = ProductImageSerializer(required=False)

    class Meta:
        model = ProductTag
        fields = ["id", "product", "tag", "tag_id", "image"]
        read_only_fields = ["id", "tag"]

    def create(self, validated_data):
        image_data = validated_data.pop("image", None)
        # validated_data now has "product": <Product>, "tag": <Tag>
        product_tag = ProductTag.objects.create(**validated_data)
        if image_data:
            product = validated_data["product"]
            image_obj = ProductImage.objects.create(product=product, **image_data)
            product_tag.image = image_obj
            product_tag.save()
        return product_tag


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    product_tags = ProductTagSerializer(many=True, required=False)

    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )
    manufacturer = serializers.StringRelatedField(read_only=True)
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(),
        source="manufacturer",
        write_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id", "name", "description", "price",
            "sales_count", "views_count", "trending_score",
            "aggregated_order_info", "current_stock", "is_launch",
            "release_date", "created_at", "updated_at",
            "images", "category", "category_id",
            "product_tags", "manufacturer", "manufacturer_id"
        )
        read_only_fields = (
            "id", "sales_count", "trending_score",
            "created_at", "updated_at","product_tags", "views_count"
        )

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        product_tags_data = validated_data.pop("product_tags", [])

        product = Product.objects.create(**validated_data)

        # Create any top-level product images
        for image_dict in images_data:
            ProductImage.objects.create(product=product, **image_dict)

        # Create any ProductTag entries (each with optional nested image)
        for tag_dict in product_tags_data:
            tag_dict["product"] = product
            nested = ProductTagSerializer(data=tag_dict)
            nested.is_valid(raise_exception=True)
            nested.save()

        return product

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
        
