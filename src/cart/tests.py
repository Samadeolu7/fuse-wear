from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from product.models import Product, Category
from cart.models import Cart, CartItem

User = get_user_model()

class CartAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a category and products
        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Smartphone",
            price=999.99,
            current_stock=10
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Laptop",
            price=1999.99,
            current_stock=5
        )

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

        # Add items to the cart
        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

    # Test: Retrieve the cart
    def test_retrieve_cart(self):
        response = self.client.get(f'/api/cart/cart/{self.cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.cart.id)
        self.assertEqual(len(response.data['items']), 2)
        self.assertEqual(response.data['total'], self.cart.get_total())

    # Test: Add a new item to the cart
    def test_add_cart_item(self):
        data = {
            "product_id": self.product1.id,
            "quantity": 3
        }
        response = self.client.post('/api/cart/cart-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product']['id'], self.product1.id)
        self.assertEqual(response.data['quantity'], 5)
    
        # Verify the cart item is associated with the user's cart
        cart_item = CartItem.objects.get(id=response.data['id'])
        self.assertEqual(cart_item.cart, self.cart)

    # Test: Update a cart item
    def test_update_cart_item(self):
        data = {
            "quantity": 5
        }
        response = self.client.patch(f'/api/cart/cart-items/{self.cart_item1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 5)

    # Test: Delete a cart item
    def test_delete_cart_item(self):
        response = self.client.delete(f'/api/cart/cart-items/{self.cart_item1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=self.cart_item1.id).exists())

    # Test: Prevent adding the same product twice
    def test_prevent_duplicate_cart_item(self):
        data = {
            "product_id": self.product1.id,
            "quantity": 1
        }
        response = self.client.post('/api/cart/cart-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 3)  # Quantity should be updated

    # Test: Check stock availability
    def test_check_stock_availability(self):
        data = {
            "product_id": self.product2.id,
            "quantity": 10  # Exceeds available stock
        }
        response = self.client.post('/api/cart/cart-items/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not enough stock", response.data['quantity']['detail'].lower())

    # Test: Retrieve cart items
    def test_retrieve_cart_items(self):
        response = self.client.get('/api/cart/cart-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test: Calculate cart total
    def test_cart_total(self):
        response = self.client.get(f'/api/cart/cart/{self.cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], self.cart.get_total())