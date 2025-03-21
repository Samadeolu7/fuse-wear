from django.test import TestCase
from product.models import Category, Product, ProductImage
from product.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer

class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Electronic gadgets")

    def test_category_serializer(self):
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data
        self.assertEqual(data['name'], "Electronics")
        self.assertEqual(data['description'], "Electronic gadgets")


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone",
            price=999.99,
            sales_count=10,
            views_count=100,
            current_stock=50
        )

    def test_product_serializer(self):
        serializer = ProductSerializer(instance=self.product)
        data = serializer.data
        self.assertEqual(data['name'], "Smartphone")
        self.assertEqual(data['price'], "999.99")
        self.assertEqual(data['sales_count'], 10)


class ProductImageSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone",
            price=999.99
        )
        self.image = ProductImage.objects.create(
            product=self.product,
            image_url="http://example.com/image.jpg",
            is_primary=True
        )

    def test_product_image_serializer(self):
        serializer = ProductImageSerializer(instance=self.image)
        data = serializer.data
        self.assertEqual(data['image_url'], "http://example.com/image.jpg")
        self.assertTrue(data['is_primary'])