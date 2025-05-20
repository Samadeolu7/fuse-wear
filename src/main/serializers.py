from rest_framework import serializers
from product.serializers import CategorySerializer, ProductSerializer


class LandingPageSerializer(serializers.Serializer):
    categories = CategorySerializer(many=True)
    bestsellers = ProductSerializer(many=True)
    trending = ProductSerializer(many=True)
    new_arrivals = ProductSerializer(many=True)

    class Meta:
        fields = ('categories', 'bestsellers', 'trending', 'new_arrivals')
        read_only_fields = ('categories', 'bestsellers', 'trending', 'new_arrivals')