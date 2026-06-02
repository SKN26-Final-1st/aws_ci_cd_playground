from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import patch_vary_headers


DEV_ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}

PROD_ALLOWED_ORIGINS = {
    "https://d2sx786sjsnbmk.cloudfront.net",
}


class DevCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")

        # 개발/운영 환경에 따라 허용 origin 목록 선택
        if settings.DEBUG:
            allowed = DEV_ALLOWED_ORIGINS
        else:
            allowed = PROD_ALLOWED_ORIGINS

        should_add_headers = origin in allowed  # ← 이게 핵심 수정 부분!

        if should_add_headers and request.method == "OPTIONS":
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