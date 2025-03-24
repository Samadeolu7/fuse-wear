from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CustomUser, UserActivity, ACTION_CHOICES


class CustomUserAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            profile_image_url="https://example.com/image.jpg",
            preferences={"theme": "dark"}
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Test creating a new user."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "confirm_password": "newpassword123",
            "profile_image_url": "https://example.com/newimage.jpg",
            "preferences": {"theme": "light"}
        }
        response = self.client.post(reverse("user-list"), data, format='json')  # Use format='json'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["email"], "newuser@example.com")

    def test_password_mismatch(self):
        """Test user creation with mismatched passwords."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "confirm_password": "wrongpassword",
        }
        response = self.client.post(reverse("user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match.", str(response.data))

    def test_retrieve_user(self):
        """Test retrieving user details."""
        response = self.client.get(reverse("user-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user(self):
        """Test updating user details."""
        data = {
            "email": "updateduser@example.com",
            "profile_image_url": "https://example.com/updatedimage.jpg",
            "preferences": {"theme": "light"}
        }
        response = self.client.patch(reverse("user-detail", args=[self.user.id]), data, format='json')  # Use format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "updateduser@example.com")
        self.assertEqual(response.data["preferences"]["theme"], "light")

    def test_retrieve_user_activities(self):
        """Test retrieving user activity logs."""
        # Create some activities for the user
        UserActivity.objects.create(user=self.user, action="login", ip_address="127.0.0.1")
        UserActivity.objects.create(user=self.user, action="logout", ip_address="127.0.0.2")
    
        response = self.client.get(reverse("user-activities", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["action"], "logout")  # Most recent activity first
        self.assertEqual(response.data[1]["action"], "login")   # Older activity second

class UserActivityAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create some activities for the user
        self.activity1 = UserActivity.objects.create(user=self.user, action="login", ip_address="127.0.0.1")
        self.activity2 = UserActivity.objects.create(user=self.user, action="logout", ip_address="127.0.0.2")

    def test_list_user_activities(self):
        """Test listing all user activities."""
        response = self.client.get(reverse("user-activity-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["action"], "logout")  # Most recent activity first
        self.assertEqual(response.data[1]["action"], "login")   # Older activity second

    def test_retrieve_user_activity(self):
        """Test retrieving a specific user activity."""
        response = self.client.get(reverse("user-activity-detail", args=[self.activity1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "login")
        self.assertEqual(response.data["ip_address"], "127.0.0.1")