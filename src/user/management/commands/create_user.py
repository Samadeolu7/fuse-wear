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
            delete = input("Do you want to delete the existing superuser? (yes/no): ").strip().lower()
            if delete == "yes":
                CustomUser.objects.filter(email=email).delete()
                self.stdout.write(self.style.SUCCESS(f"Superuser with email '{email}' deleted successfully!"))
                # Create the superuser again
                user = CustomUser(
                    username="admin",
                    email=email,
                )
                user.set_password(password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Superuser with email '{email}' created successfully!"))
                
            else:
                self.stdout.write(self.style.SUCCESS(f"Superuser with email '{email}' not deleted."))
        else:
            # Create the superuser
            user = CustomUser(
                username="admin",
                email=email,
            )
            user.set_password(password)  # Hash the password
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser with email '{email}' created successfully!"))