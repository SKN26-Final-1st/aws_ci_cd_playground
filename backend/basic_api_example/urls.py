from django.urls import path

from . import views


urlpatterns = [
    path("ping/", views.ping, name="basic-ping"),
    path("echo/", views.echo, name="basic-echo"),
]
