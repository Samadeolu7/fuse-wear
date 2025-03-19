from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from product.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        help_text="Rating from 1 to 5",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(1000, "Comment cannot exceed 1000 characters.")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product', 'created_at']),
            models.Index(fields=['user']),  # Optional: Add index for user queries
        ]
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_review_per_user')
        ]

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name} (Rating: {self.rating})"