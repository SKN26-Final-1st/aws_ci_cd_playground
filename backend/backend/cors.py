from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import patch_vary_headers


DEV_ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}


class DevCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        # 개발 중인 Vite 주소에서 온 요청에만 CORS 응답 헤더를 붙입니다.
        should_add_headers = settings.DEBUG and origin in DEV_ALLOWED_ORIGINS

        if should_add_headers and request.method == "OPTIONS":
            # 브라우저가 실제 POST 전에 보내는 preflight 요청은 바로 204로 응답합니다.
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        if should_add_headers:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = (
                "Content-Type, X-CSRFToken, Authorization"
            )
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            patch_vary_headers(response, ("Origin",))

        return response
