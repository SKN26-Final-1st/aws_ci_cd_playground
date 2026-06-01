from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_view, name="jwt-login"),
    path("me/", views.me, name="jwt-me"),
    path("protected/", views.protected, name="jwt-protected"),
]
