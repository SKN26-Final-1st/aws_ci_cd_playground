from django.conf import settings
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from backend.api import json_error, method_not_allowed, parse_json_body
from backend.demo_users import authenticate_demo_user, serialize_user


@ensure_csrf_cookie
def csrf(request):
    # React가 세션 로그인 POST를 보내기 전에 CSRF 쿠키를 받을 수 있게 하는 API입니다.
    if request.method != "GET":
        return method_not_allowed(["GET"])

    return JsonResponse(
        {
            "ok": True,
            "csrfCookieName": settings.CSRF_COOKIE_NAME,
            "csrfHeaderName": "X-CSRFToken",
            "csrfToken": get_token(request),
        }
    )


def login_view(request):
    if request.method != "POST":
        return method_not_allowed(["POST"])

    # React 로그인 폼에서 보낸 username/password JSON을 꺼냅니다.
    data = parse_json_body(request)
    if data is None:
        return json_error("Invalid JSON body", status=400)

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return json_error("Username and password are required", status=400)

    user = authenticate_demo_user(request, username, password)
    if user is None:
        return json_error("Invalid credentials", status=401)

    # Django 세션에 사용자 id를 저장하고, 브라우저에는 sessionid 쿠키가 내려갑니다.
    login(request, user)
    return JsonResponse(
        {
            "ok": True,
            "auth": "session",
            "user": serialize_user(user),
        }
    )


def logout_view(request):
    if request.method != "POST":
        return method_not_allowed(["POST"])

    # 서버 세션을 비워서 같은 쿠키로 다시 보호 API를 호출해도 인증되지 않게 합니다.
    logout(request)
    return JsonResponse({"ok": True, "authenticated": False, "user": None})


def me(request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    # AuthenticationMiddleware가 sessionid 쿠키를 보고 request.user를 채워줍니다.
    if not request.user.is_authenticated:
        return JsonResponse({"ok": True, "authenticated": False, "user": None})

    return JsonResponse(
        {
            "ok": True,
            "authenticated": True,
            "user": serialize_user(request.user),
        }
    )


def protected(request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    if not request.user.is_authenticated:
        return json_error("Authentication required", status=403)

    # 인가가 필요한 API 예시입니다. 로그인된 사용자에게만 데이터를 내려줍니다.
    return JsonResponse(
        {
            "ok": True,
            "message": "session secret",
            "user": serialize_user(request.user),
        }
    )
