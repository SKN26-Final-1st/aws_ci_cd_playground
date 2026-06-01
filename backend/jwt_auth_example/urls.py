from django.urls import path
from .views import JwtLoginView, JwtRefreshView, ProtectedView

urlpatterns = [
    path("login/",     JwtLoginView.as_view()),
    path("refresh/",   JwtRefreshView.as_view()),
    path("protected/", ProtectedView.as_view()),
]
