import os
from django.core.management.base import BaseCommand
from product.models import Category, Manufacturer, Product, ProductImage, Tag
from django.utils.timezone import now
from django.conf import settings

class Command(BaseCommand):
    help = "Delete all existing products and categories, then create new ones along with tags."

    def handle(self, *args, **kwargs):
        # Delete all existing products, categories, and tags
        self.stdout.write("Deleting all existing products, categories, and tags...")
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All existing products, categories, and tags deleted successfully."))

        # Ensure the media directory exists
        media_dir = os.path.join(settings.MEDIA_ROOT, "product_images")
        os.makedirs(media_dir, exist_ok=True)

        # Create Categories
        categories = {
            "Men": "Men's clothing and accessories",
            "Women": "Women's clothing and accessories",
            "Children": "Children's clothing and accessories",
            "Accessories": "General accessories",
        }
        category_objects = {}
        for name, description in categories.items():
            category, _ = Category.objects.get_or_create(name=name, description=description)
            category_objects[name] = category

        # Create Tags
        tags = [
            {"name": "Size", "value": "Small"},
            {"name": "Size", "value": "Medium"},
            {"name": "Size", "value": "Large"},
            {"name": "Color", "value": "Red"},
            {"name": "Color", "value": "Blue"},
            {"name": "Color", "value": "Green"},
        ]
        tag_objects = {}
        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_data["name"], value=tag_data["value"])
            tag_objects[f"{tag_data['name']}_{tag_data['value']}"] = tag

        manufacturer, _ = Manufacturer.objects.get_or_create(
            name="Demo Manufacturer",
            defaults={
                "address": "123 Demo Street",
                "contact_email": "demo@example.com",
                "contact_phone": "1234567890"
            }
        )
        # Create Products for Men and Women
        products = [
            {
                "category": category_objects["Men"],
                "name": "Men's T-Shirt",
                "description": "A comfortable men's t-shirt.",
                "price": 19.99,
                "sales_count": 100,
                "views_count": 200,
                "trending_score": 80.0,
                "current_stock": 50,
                "is_launch": True,
                "release_date": now(),
                "tags": [tag_objects["Size_Medium"], tag_objects["Color_Blue"]],
                "images": [
                    {"image_name": "mens_tshirt.jpg", "is_primary": True},
                ],
                "manufacturer": manufacturer,
            },
            {
                "category": category_objects["Men"],
                "name": "Men's Jeans",
                "description": "Stylish men's jeans.",
                "price": 49.99,
                "sales_count": 80,
                "views_count": 150,
                "trending_score": 70.0,
                "current_stock": 40,
                "is_launch": True,
                "release_date": now(),
                "tags": [tag_objects["Size_Large"], tag_objects["Color_Blue"]],
                "images": [
                    {"image_name": "mens_jeans.jpg", "is_primary": True},
                ],
                "manufacturer": manufacturer,
            },
            {
                "category": category_objects["Women"],
                "name": "Women's Dress",
                "description": "A beautiful women's dress.",
                "price": 39.99,
                "sales_count": 120,
                "views_count": 250,
                "trending_score": 90.0,
                "current_stock": 30,
                "is_launch": True,
                "release_date": now(),
                "tags": [tag_objects["Size_Small"], tag_objects["Color_Red"]],
                "images": [
                    {"image_name": "womens_dress.jpg", "is_primary": True},
                ],
                "manufacturer": manufacturer,
            },
            {
                "category": category_objects["Women"],
                "name": "Women's Handbag",
                "description": "A stylish women's handbag.",
                "price": 59.99,
                "sales_count": 60,
                "views_count": 100,
                "trending_score": 75.0,
                "current_stock": 20,
                "is_launch": True,
                "release_date": now(),
                "tags": [tag_objects["Color_Green"]],
                "images": [
                    {"image_name": "womens_handbag.jpg", "is_primary": True},
                ],
                "manufacturer": manufacturer,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                category=product_data["category"],
                name=product_data["name"],
                manufacturer=product_data["manufacturer"],
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

            # Add tags to the product
            product.tags.set(product_data["tags"])

            # Add images for the product
            for image_data in product_data["images"]:
                image_path = os.path.join(media_dir, image_data["image_name"])
                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f"Image file '{image_data['image_name']}' not found. Skipping."))
                    continue

                ProductImage.objects.get_or_create(
                    product=product,
                    image=f"product_images/{image_data['image_name']}",
                    is_primary=image_data["is_primary"],
                )

        self.stdout.write(self.style.SUCCESS("Categories, products, and tags created successfully!"))