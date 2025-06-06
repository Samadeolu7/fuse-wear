from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderItem._meta.get_field('product').related_model.objects.all(),
        source='product',
        write_only=True
    )
    product = ProductSerializer(read_only=True)
    order = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = OrderItem
        fields = [
            'id', 'order','product', 'product_id', 'name', 'quantity', 'price', 'color', 'size'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)


    class Meta:
        model = Order
        fields = [
            'id', 'user', 'payment_intent_id', 'amount', 'currency',
            'shipping_info', 'subtotal', 'shipping', 'total', 'status', 'tracking_number', 'tracking_url',
            'created_at', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order