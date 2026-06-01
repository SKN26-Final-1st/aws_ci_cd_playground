from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.api import json_error, method_not_allowed, parse_json_body
from backend.demo_users import authenticate_demo_user, serialize_user

from .tokens import TokenError, create_access_token, verify_access_token


def _bearer_token(request):
    # JWT 방식에서는 쿠키 대신 Authorization 헤더에서 Bearer 토큰을 꺼냅니다.
    authorization = request.headers.get("Authorization", "")
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        return None

    token = authorization[len(prefix) :].strip()
    return token or None


def _authenticated_user_from_bearer(request):
    token = _bearer_token(request)
    if token is None:
        return None, "Bearer token required"

    try:
        # 서명과 만료 시간이 맞는 토큰이면 Django User 객체를 돌려받습니다.
        return verify_access_token(token), None
    except TokenError:
        return None, "Invalid token"


@csrf_exempt
def login_view(request):
    # Bearer 토큰 로그인은 쿠키 세션을 쓰지 않으므로 CSRF 검사 없이 JSON POST를 받습니다.
    if request.method != "POST":
        return method_not_allowed(["POST"])

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

    # 로그인 성공 시 React가 보관할 access token을 응답 body로 내려줍니다.
    return JsonResponse(
        {
            "ok": True,
            "auth": "jwt",
            "accessToken": create_access_token(user),
            "tokenType": "Bearer",
            "user": serialize_user(user),
        }
    )


def me(request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    user, error = _authenticated_user_from_bearer(request)
    if error is not None:
        return json_error(error, status=401)

    # 토큰이 가리키는 사용자가 누구인지 확인하는 API입니다.
    return JsonResponse({"ok": True, "authenticated": True, "user": serialize_user(user)})


def protected(request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    user, error = _authenticated_user_from_bearer(request)
    if error is not None:
        return json_error(error, status=401)

    # Authorization 헤더의 토큰이 유효할 때만 접근 가능한 보호 API입니다.
    return JsonResponse(
        {
            "ok": True,
            "message": "jwt secret",
            "user": serialize_user(user),
        }
    )
