"""
backend/backend/cors.py
로컬 개발 전용 CORS 미들웨어 (DEBUG=True 일 때만 MIDDLEWARE에 들어감)
"""


class DevCorsMiddleware:
    ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        origin = request.META.get("HTTP_ORIGIN", "")
        if origin in self.ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type,X-CSRFToken"
        return response
