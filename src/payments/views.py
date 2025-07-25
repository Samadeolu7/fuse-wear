from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .models import Payment
from .serializers import PaymentSerializer, CreatePaymentIntentSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse, inline_serializer

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


class StripeWebhookView(generics.GenericAPIView):
    """
    Handles Stripe webhook events for payment processing.
    """
    authentication_classes = []  # No auth for webhooks
    permission_classes = []      # No permissions for webhooks
    
    class WebhookSerializer(serializers.Serializer):
        id = serializers.CharField(help_text="Stripe event ID")
        type = serializers.CharField(help_text="Stripe event type")
        data = serializers.DictField(help_text="Event data object")
    
    serializer_class = WebhookSerializer

    @csrf_exempt
    @extend_schema(
        summary="Stripe Webhook Endpoint",
        description="Handles Stripe webhook events for payment processing",
        request=WebhookSerializer,
        responses={
            200: OpenApiResponse(
                description="Webhook processed successfully",
                examples=[
                    OpenApiExample(
                        "Success",
                        value={"status": "success", "message": "Webhook handled successfully"}
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid payload",
                examples=[
                    OpenApiExample(
                        "Invalid Signature",
                        value={"error": "Invalid signature"}
                    )
                ]
            ),
            500: OpenApiResponse(description="Server error")
        },
        tags=['Payments']
    )
    def post(self, request):
        """
        Handles Stripe webhook events for payment processing.
        Validates the webhook signature and processes various event types.
        
        Required headers:
        - Stripe-Signature: Webhook signature for verification
        
        Handles events:
        - payment_intent.succeeded: Confirms successful payment
        - payment_intent.payment_failed: Handles failed payments
        - charge.refunded: Processes refunds
        """
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
            user_id = intent.metadata.get("user_id")

            Payment.objects.create(
                user_id=user_id,
                order_id=order_id,
                stripe_payment_intent_id=intent.id,
                amount=intent.amount / 100,
                currency=intent.currency,
                status=intent.status,
            )
        elif event['type'] == 'payment_intent.payment_failed':
            intent = event['data']['object']
            
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