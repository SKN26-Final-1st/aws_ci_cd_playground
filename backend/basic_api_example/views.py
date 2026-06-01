from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.api import json_error, method_not_allowed, parse_json_body


def ping(request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    # 가장 단순한 연결 확인용 API입니다. React에서 GET 요청 연습에 씁니다.
    return JsonResponse(
        {
            "ok": True,
            "message": "pong from Django",
            "method": request.method,
        }
    )


@csrf_exempt
def echo(request):
    # 로그인/쿠키와 무관한 공개 POST 예제라서 CSRF 검사를 끕니다.
    if request.method != "POST":
        return method_not_allowed(["POST"])

    data = parse_json_body(request)
    if data is None:
        return json_error("Invalid JSON body", status=400)

    # React가 보낸 JSON body를 그대로 돌려줘서 요청 body 구조를 확인할 수 있습니다.
    return JsonResponse({"ok": True, "received": data})
