from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, UserActivityViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'user-activities', UserActivityViewSet, basename='user-activity')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

