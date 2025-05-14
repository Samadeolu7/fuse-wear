from rest_framework import serializers

class CreatePaymentIntentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=50)  # amount in cents
    currency = serializers.CharField(default="aud")
    metadata = serializers.DictField(child=serializers.CharField(), required=False)

from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'stripe_payment_intent_id', 'amount', 'currency', 'status', 'created_at']