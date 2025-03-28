from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Metrics for dynamic sections
    sales_count = models.PositiveIntegerField(default=0, db_index=True)
    views_count = models.PositiveIntegerField(default=0)
    trending_score = models.FloatField(default=0.0, db_index=True)
    
    # Aggregated order information
    aggregated_order_info = models.JSONField(blank=True, null=True)

    # Inventory and launch details
    current_stock = models.PositiveIntegerField(default=0, db_index=True)
    is_launch = models.BooleanField(default=False, db_index=True)
    release_date = models.DateTimeField(blank=True, null=True, db_index=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sales_count']),
            models.Index(fields=['trending_score']),
            models.Index(fields=['release_date']),
            models.Index(fields=['current_stock']),
            models.Index(fields=['is_launch']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_released(self):
        return self.release_date and self.release_date <= timezone.now()

    def is_in_stock(self):
        return self.current_stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(validators=[URLValidator()])
    media_type = models.CharField(max_length=50, help_text="e.g., image/jpeg, image/png")
    alt_text = models.CharField(max_length=255, blank=True, default="Image")
    is_primary = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product'], condition=models.Q(is_primary=True), name='unique_primary_image_per_product')
        ]

    def __str__(self):
        return f"Image for {self.product.name} ({'Primary' if self.is_primary else 'Secondary'})"