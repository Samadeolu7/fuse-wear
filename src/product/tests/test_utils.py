from django.test import TestCase
from product.utils import compute_trending_score, aggregate_order_info
from product.models import Product

class UtilsTest(TestCase):
    def test_compute_trending_score(self):
        score = compute_trending_score(sales_count=10, views_count=100, weight_sales=0.7, weight_views=0.3)
        self.assertEqual(score, 37.0)

    def test_aggregate_order_info(self):
        product = Product(name="Smartphone", price=999.99, sales_count=10)
        info = aggregate_order_info(product)
        self.assertEqual(info['total_revenue'], 9999.9)
        self.assertEqual(info['total_orders'], 10)