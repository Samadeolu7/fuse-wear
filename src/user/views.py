# user/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, UserActivity
from .serializers import CustomUserSerializer, UserActivitySerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Provides endpoints for listing, retrieving, updating, and deleting users.
    Also includes a custom endpoint to retrieve user activity logs.
    """
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Return the activity log for a specific user."""
        user = self.get_object()
        activities = user.activities.all()
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only endpoints to list and retrieve user activities.
    """
    queryset = UserActivity.objects.all().order_by('-timestamp')
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]
