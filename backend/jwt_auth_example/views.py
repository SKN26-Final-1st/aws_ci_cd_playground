import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(View):
    """GET 하면 csrftoken 쿠키를 심어준다."""
    def get(self, request):
        return JsonResponse({"detail": "CSRF cookie set"})


class LoginView(View):
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

        login(request, user)
        return JsonResponse({"detail": "logged in", "username": user.username})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"detail": "logged out"})


class MeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "not authenticated"}, status=401)
        return JsonResponse({"username": request.user.username, "email": request.user.email})
