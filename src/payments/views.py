from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .models import Payment
from .serializers import PaymentSerializer
from .serializers import CreatePaymentIntentSerializer

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import stripe


import stripe
from django.conf import settings

from drf_spectacular.utils import extend_schema

class CreatePaymentIntentView(APIView):
    @extend_schema(
        request=CreatePaymentIntentSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "clientSecret": {"type": "string", "description": "The client secret for the payment intent."}
                },
            }
        },
        description="Create a Stripe Payment Intent for one-time payments.",
    )
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Set the API key

        serializer = CreatePaymentIntentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        intent = stripe.PaymentIntent.create(
            amount=data["amount"],
            currency=data["currency"],
            metadata=data.get("metadata", {}),
        )
        return Response({"clientSecret": intent.client_secret})


@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent.metadata.get("order_id")
        user_id = intent.metadata.get("user_id")  # Optional: Pass user_id in metadata

        # Save payment data to the database
        Payment.objects.create(
            user_id=user_id,
            order_id=order_id,
            stripe_payment_intent_id=intent.id,
            amount=intent.amount / 100,  # Convert cents to dollars
            currency=intent.currency,
            status=intent.status,
        )
    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        # Handle failed payment (optional)
        Payment.objects.create(
            stripe_payment_intent_id=intent.id,
            amount=intent.amount / 100,
            currency=intent.currency,
            status=intent.status,
        )

    return Response(status=status.HTTP_200_OK)


class PaymentHistoryView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')