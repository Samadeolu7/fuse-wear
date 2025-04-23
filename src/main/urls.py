from django.urls import path
from .views import landing_page, ping

urlpatterns = [
    path("ping/", ping, name="ping"),
    path("", landing_page, name="landing_page"),
]