import json

from django.http import JsonResponse


def json_error(message, status=400):
    # 모든 예제 API가 같은 모양의 JSON 에러를 내려주도록 맞춥니다.
    return JsonResponse({"ok": False, "error": message}, status=status)


def method_not_allowed(allowed_methods):
    # 잘못된 HTTP method로 호출했을 때 허용 method를 같이 알려줍니다.
    return JsonResponse(
        {
            "ok": False,
            "error": "Method not allowed",
            "allowedMethods": allowed_methods,
        },
        status=405,
    )


def parse_json_body(request):
    # Django의 request.body는 bytes라서 JSON 문자열로 디코딩한 뒤 dict로 바꿉니다.
    if not request.body:
        return {}

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None

    # 이 학습 예제에서는 JSON object만 허용하고, 배열/문자열 body는 잘못된 요청으로 봅니다.
    return data if isinstance(data, dict) else None
