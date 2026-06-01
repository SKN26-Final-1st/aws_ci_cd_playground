import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView


class JwtLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"detail": "invalid JSON"}, status=400)

        user = authenticate(
            request,
            username=data.get("username"),
            password=data.get("password"),
        )
        if user is None:
            return JsonResponse({"detail": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            "access":  str(refresh.access_token),
            "refresh": str(refresh),
        })


class JwtRefreshView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            refresh = RefreshToken(data["refresh"])
        except (KeyError, TokenError):
            return JsonResponse({"detail": "Invalid or missing refresh token"}, status=401)
        return JsonResponse({"access": str(refresh.access_token)})


class ProtectedView(View):
    """Authorization: Bearer <access_token> 헤더가 있어야 접근 가능"""
    def get(self, request):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework.exceptions import AuthenticationFailed
        try:
            auth = JWTAuthentication()
            validated = auth.authenticate(request)
            if validated is None:
                raise AuthenticationFailed
            user, _ = validated
        except Exception:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        return JsonResponse({"message": f"Hello, {user.username}! This is JWT-protected."})
