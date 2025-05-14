from django.urls import path
from .views import CreatePaymentIntentView, stripe_webhook, PaymentHistoryView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment-history'),
]
