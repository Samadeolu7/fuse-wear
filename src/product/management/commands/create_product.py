import os
from django.core.management.base import BaseCommand
from product.models import Category, Product, ProductImage
from django.utils.timezone import now
from django.conf import settings

class Command(BaseCommand):
    help = "Create 5 sample products with images"

    def handle(self, *args, **kwargs):
        # Ensure the media directory exists
        media_dir = os.path.join(settings.MEDIA_ROOT, "product_images")
        os.makedirs(media_dir, exist_ok=True)

        # Create Categories
        electronics = Category.objects.get_or_create(name="Electronics", description="Electronic items")[0]
        fashion = Category.objects.get_or_create(name="Fashion", description="Clothing and accessories")[0]

        # Create Products
        products = [
            {
                "category": electronics,
                "name": "Smartphone1",
                "description": "A high-end smartphone with great features.",
                "price": 999.99,
                "sales_count": 500,
                "views_count": 1000,
                "trending_score": 95.0,
                "current_stock": 50,
                "is_launch": True,
                "release_date": now(),
                "images": [
                    {"image_name": "1.jpg", "is_primary": True},
                    {"image_name": "2.jpg", "is_primary": False},
                ],
            },
            {
                "category": electronics,
                "name": "Laptop1",
                "description": "A powerful laptop for professionals.",
                "price": 1999.99,
                "sales_count": 300,
                "views_count": 800,
                "trending_score": 85.0,
                "current_stock": 30,
                "is_launch": False,
                "release_date": now(),
                "images": [
                    {"image_name": "3.jpg", "is_primary": True},
                ],
            },
            {
                "category": fashion,
                "name": "Designer Jacket1",
                "description": "A stylish designer jacket for winter.",
                "price": 199.99,
                "sales_count": 200,
                "views_count": 500,
                "trending_score": 75.0,
                "current_stock": 20,
                "is_launch": True,
                "release_date": now(),
                "images": [
                    {"image_name": "4.jpg", "is_primary": True},
                ],
            },
            {
                "category": electronics,
                "name": "Smartwatch1",
                "description": "A smartwatch with fitness tracking features.",
                "price": 299.99,
                "sales_count": 150,
                "views_count": 400,
                "trending_score": 70.0,
                "current_stock": 25,
                "is_launch": True,
                "release_date": now(),
                "images": [
                    {"image_name": "5.jpg", "is_primary": True},
                ],
            },
            {
                "category": fashion,
                "name": "Sneakers1",
                "description": "Comfortable and stylish sneakers.",
                "price": 99.99,
                "sales_count": 100,
                "views_count": 300,
                "trending_score": 60.0,
                "current_stock": 40,
                "is_launch": False,
                "release_date": now(),
                "images": [
                    {"image_name": "6.jpg", "is_primary": True},
                ],
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                category=product_data["category"],
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "sales_count": product_data["sales_count"],
                    "views_count": product_data["views_count"],
                    "trending_score": product_data["trending_score"],
                    "current_stock": product_data["current_stock"],
                    "is_launch": product_data["is_launch"],
                    "release_date": product_data["release_date"],
                },
            )

            # Add images for the product
            for image_data in product_data["images"]:
                image_path = os.path.join(media_dir, image_data["image_name"])
                print(f"Checking for image file: {image_path}")
                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f"Image file '{image_data['image_name']}' not found. Skipping."))
                    continue

                ProductImage.objects.get_or_create(
                    product=product,
                    image=f"product_images/{image_data['image_name']}",
                    is_primary=image_data["is_primary"],
                )

        self.stdout.write(self.style.SUCCESS("5 sample products with images created successfully!"))