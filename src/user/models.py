from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    # Additional profile fields
    profile_image_url = models.URLField(blank=True, null=True)
    # Personalization metadata (e.g., user preferences)
    preferences = models.JSONField(blank=True, null=True)

    def clean(self):
        super().clean()
        if self.profile_image_url:
            validator = URLValidator()
            try:
                validator(self.profile_image_url)
            except ValidationError:
                raise ValidationError("Invalid profile image URL.")

    def __str__(self):
        return self.username


ACTION_CHOICES = [
    ('login', 'Login'),
    ('logout', 'Logout'),
    ('update_profile', 'Update Profile'),
    ('purchase', 'Purchase'),
    # Add more as needed
]

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    # Extra metadata to help with personalization
    meta_data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
        ordering = ['-timestamp']
        constraints = [
            models.CheckConstraint(
                check=models.Q(action__in=[choice[0] for choice in ACTION_CHOICES]),
                name="valid_action"
            ),
        ]

    def __str__(self):
        # Format timestamp for better readability
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.user.username} - {self.action} at {formatted_timestamp}"