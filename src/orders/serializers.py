from rest_framework import serializers
from .models import Manufacturer, Order, OrderItem
from product.serializers import ProductSerializer

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderItem._meta.get_field('product').related_model.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'product_id', 'name', 'quantity', 'price', 'color', 'size'
        ]
        read_only_fields = ('id', 'order', 'product')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)


    class Meta:
        model = Order
        fields = [
            'id', 'user', 'payment_intent_id', 'amount', 'currency',
            'shipping_info', 'subtotal', 'shipping', 'total', 'status', 'tracking_number', 'tracking_url',
            'created_at', 'items'
        ]
        read_only_fields = ('id', 'created_at', 'items', 'manufacturer')