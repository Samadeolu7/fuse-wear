from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Category, Product

class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone",
            price=999.99,
            sales_count=10,
            views_count=100,
            current_stock=50
        )

    def test_get_products(self):
        response = self.client.get('/api/product/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        response = self.client.get(f'/api/product/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smartphone")

    def test_bestsellers(self):
        response = self.client.get('/api/product/products/bestsellers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_trending(self):
        response = self.client.get('/api/product/products/trending/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)