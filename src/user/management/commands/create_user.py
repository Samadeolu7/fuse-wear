from django.core.management.base import BaseCommand
from user.models import CustomUser

class Command(BaseCommand):
    help = "Create a superuser with predefined credentials"

    def handle(self, *args, **kwargs):
        email = "admin@gmail.com"
        password = "password677"

        # Check if the superuser already exists
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superuser with email '{email}' already exists."))
        else:
            # Create the superuser
            CustomUser.objects.create_superuser(
                username="admin",
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser with email '{email}' created successfully!"))