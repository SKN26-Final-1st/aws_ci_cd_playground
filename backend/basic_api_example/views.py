import json
from django.utils import timezone
from django.http import JsonResponse
from django.views import View


class PingView(View):
    def get(self, request):
        return JsonResponse({
            "message": "pong",
            "server_time": timezone.now().isoformat(),
        })


class EchoView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
        except Exception:
            body = {}
        return JsonResponse({"echo": body})
