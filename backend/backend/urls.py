"""
backend/backend/urls.py
모든 API는 /api/ 아래에 두어 nginx가 /api/ → Django 로 분기합니다.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/basic/",   include("basic_api_example.urls")),
    path("api/session/", include("session_auth_example.urls")),
    path("api/jwt/",     include("jwt_auth_example.urls")),
]
