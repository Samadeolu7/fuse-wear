from django.urls import path
from .views import CreatePaymentIntentView, StripeWebhookView, PaymentHistoryView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment-history'),
]