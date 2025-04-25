# filepath: /d:/Users/User/Desktop/Michael/src/product/management/commands/create_sample_products.py
from django.core.management.base import BaseCommand
from product.models import Category, Product
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Create sample products for testing"

    def handle(self, *args, **kwargs):
        # Create Categories
        electronics = Category.objects.get_or_create(name="Electronics", description="Electronic items")[0]
        fashion = Category.objects.get_or_create(name="Fashion", description="Clothing and accessories")[0]
        home_appliances = Category.objects.get_or_create(name="Home Appliances", description="Appliances for home use")[0]

        # Create Products
        Product.objects.get_or_create(
            category=electronics,
            name="Smartphone",
            description="A high-end smartphone with great features.",
            price=999.99,
            sales_count=500,
            views_count=1000,
            trending_score=95.0,
            current_stock=50,
            is_launch=True,
            release_date=now()
        )

        Product.objects.get_or_create(
            category=electronics,
            name="Laptop",
            description="A powerful laptop for professionals.",
            price=1999.99,
            sales_count=300,
            views_count=800,
            trending_score=85.0,
            current_stock=30,
            is_launch=False,
            release_date=now()
        )

        Product.objects.get_or_create(
            category=fashion,
            name="Designer Jacket",
            description="A stylish designer jacket for winter.",
            price=199.99,
            sales_count=200,
            views_count=500,
            trending_score=75.0,
            current_stock=20,
            is_launch=True,
            release_date=now()
        )

        Product.objects.get_or_create(
            category=home_appliances,
            name="Microwave Oven",
            description="A compact microwave oven for quick cooking.",
            price=149.99,
            sales_count=100,
            views_count=300,
            trending_score=65.0,
            current_stock=10,
            is_launch=False,
            release_date=now()
        )

        Product.objects.get_or_create(
            category=home_appliances,
            name="Vacuum Cleaner",
            description="A powerful vacuum cleaner for home cleaning.",
            price=299.99,
            sales_count=50,
            views_count=200,
            trending_score=55.0,
            current_stock=5,
            is_launch=True,
            release_date=now()
        )

        self.stdout.write(self.style.SUCCESS("Sample products created successfully!"))