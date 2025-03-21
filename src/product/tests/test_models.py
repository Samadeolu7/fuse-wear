from django.test import TestCase
from django.utils import timezone
from product.models import Category, Product, ProductImage

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Electronic gadgets")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.description, "Electronic gadgets")
        self.assertIsNotNone(self.category.created_at)

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), "Electronics")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone",
            description="A high-end smartphone",
            price=999.99,
            sales_count=10,
            views_count=100,
            current_stock=50,
            release_date=timezone.now()
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.sales_count, 10)
        self.assertTrue(self.product.is_in_stock())
        self.assertTrue(self.product.is_released())

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), "Smartphone")


class ProductImageModelTest(TestCase):
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

    def test_product_image_creation(self):
        self.assertEqual(self.image.product, self.product)
        self.assertEqual(self.image.image_url, "http://example.com/image.jpg")
        self.assertTrue(self.image.is_primary)

    def test_product_image_string_representation(self):
        self.assertEqual(str(self.image), "Image for Smartphone (Primary)")