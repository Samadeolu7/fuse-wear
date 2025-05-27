from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from product.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Cart for {self.user.username} (Created: {self.created_at.strftime('%Y-%m-%d')})"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_color = models.CharField(max_length=50, blank=True, default="Default")
    selected_size = models.CharField(max_length=50, blank=True, default="Default")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ]
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity} of {self.product.name} (${self.get_subtotal():.2f}) in {self.cart.user.username}'s cart"

    def get_subtotal(self):
        return self.product.price * self.quantity

    def is_in_stock(self):
        return self.product.current_stock >= self.quantity