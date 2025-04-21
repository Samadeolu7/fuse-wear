from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.urls import include, path

from .views import CustomUserViewSet, UserActivityViewSet
from .views import RegisterView


router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'user-activities', UserActivityViewSet, basename='user-activity')

urlpatterns = [
    path('', include(router.urls)),
     # JWT Authentication Endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Registration Endpoint
    path('auth/register/', RegisterView.as_view(), name='register'),
]

