from rest_framework import viewsets, permissions
from .models import Manufacturer, Order, OrderItem
from .serializers import ManufacturerSerializer, OrderSerializer, OrderItemSerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('manufacturer', 'user').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Users see their own orders; staff see all
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all().select_related('order', 'product')
#     serializer_class = OrderItemSerializer
#     permission_classes = [permissions.IsAuthenticated]