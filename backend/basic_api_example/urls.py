from django.urls import path
from .views import PingView, EchoView

urlpatterns = [
    path("ping/", PingView.as_view()),
    path("echo/", EchoView.as_view()),
]
