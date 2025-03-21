from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product.models import Category, Product, ProductImage

class ProductAPITestCase(APITestCase):
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(name="Electronics", description="Electronic gadgets")

        # Create products
        self.product1 = Product.objects.create(
            category=self.category,
            name="Smartphone",
            description="A high-end smartphone",
            price=999.99,
            sales_count=50,
            views_count=200,
            current_stock=10,
            release_date=timezone.now()
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="A powerful laptop",
            price=1999.99,
            sales_count=30,
            views_count=150,
            current_stock=5,
            release_date=timezone.now()
        )

        # Create product images
        self.image1 = ProductImage.objects.create(
            product=self.product1,
            image_url="http://example.com/smartphone.jpg",
            is_primary=True
        )
        self.image2 = ProductImage.objects.create(
            product=self.product2,
            image_url="http://example.com/laptop.jpg",
            is_primary=True
        )

        # API client
        self.client = APIClient()

    # Test: List all products
    def test_list_products(self):
        response = self.client.get('/api/product/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Laptop")
        self.assertEqual(response.data[1]['name'], "Smartphone")

    # Test: Retrieve a single product
    def test_retrieve_product(self):
        response = self.client.get(f'/api/product/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smartphone")
        self.assertEqual(response.data['price'], "999.99")

    # Test: Create a new product
    def test_create_product(self):
        data = {
            "name": "Tablet",
            "description": "A lightweight tablet",
            "price": 499.99,
            "category_id": self.category.id,
            "current_stock": 20,
            "release_date": timezone.now().isoformat()
        }
        response = self.client.post('/api/product/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Tablet")
        self.assertEqual(response.data['price'], "499.99")

    # Test: Update a product
    def test_update_product(self):
        data = {
            "name": "Smartphone Pro",
            "price": 1099.99
        }
        response = self.client.patch(f'/api/product/products/{self.product1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smartphone Pro")
        self.assertEqual(response.data['price'], "1099.99")

    # Test: Delete a product
    def test_delete_product(self):
        response = self.client.delete(f'/api/product/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    # Test: Bestsellers endpoint
    def test_bestsellers(self):
        response = self.client.get('/api/product/products/bestsellers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Smartphone")  # Highest sales_count

    # Test: Trending endpoint
    def test_trending(self):
        response = self.client.get('/api/product/products/trending/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Laptop")  # Highest trending_score

    # Test: New arrivals endpoint
    def test_new_arrivals(self):
        response = self.client.get('/api/product/products/new_arrivals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Laptop")  # Most recent release_date

    # Test: Search products
    def test_search_products(self):
        response = self.client.get('/api/product/products/?search=Smartphone')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Smartphone")

    # Test: Filter products by category
    def test_filter_products_by_category(self):
        response = self.client.get(f'/api/product/products/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test: Order products by price
    def test_order_products_by_price(self):
        response = self.client.get('/api/product/products/?ordering=price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "Smartphone")  # Lowest price first
        self.assertEqual(response.data[1]['name'], "Laptop")      # Highest price last