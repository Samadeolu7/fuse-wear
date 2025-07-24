from django.urls import path
from .views import LandingPageView, ping

urlpatterns = [
    path('ping/', ping, name='ping'),
    path('landing/', LandingPageView.as_view(), name='landing_page'),
]