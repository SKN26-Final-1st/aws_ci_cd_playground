import base64
import hashlib
import hmac
import json
import time

from django.conf import settings
from django.contrib.auth import get_user_model


class TokenError(Exception):
    # 토큰 검증 실패를 view에서 401 응답으로 바꾸기 위해 사용하는 예외입니다.
    pass


def _base64url_encode(data):
    # JWT는 일반 base64가 아니라 URL에 안전한 base64url 형식을 사용합니다.
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}".encode("ascii"))


def _json_part(data):
    # header/payload dict를 JSON 문자열로 만든 뒤 JWT 조각으로 인코딩합니다.
    return _base64url_encode(
        json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )


def _signature(signing_input):
    # header.payload 문자열을 SECRET_KEY로 서명해서 위조 여부를 확인할 수 있게 합니다.
    return _base64url_encode(
        hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            signing_input.encode("ascii"),
            hashlib.sha256,
        ).digest()
    )


def create_access_token(user, expires_in_seconds=3600):
    now = int(time.time())
    # header는 토큰 종류와 서명 알고리즘, payload는 사용자와 만료 정보를 담습니다.
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user.id),
        "username": user.get_username(),
        "iat": now,
        "exp": now + expires_in_seconds,
    }
    signing_input = f"{_json_part(header)}.{_json_part(payload)}"

    # 최종 JWT 형태는 header.payload.signature 입니다.
    return f"{signing_input}.{_signature(signing_input)}"


def verify_access_token(token):
    parts = token.split(".")
    if len(parts) != 3:
        raise TokenError("Invalid token")

    signing_input = f"{parts[0]}.{parts[1]}"
    expected_signature = _signature(signing_input)
    # compare_digest는 문자열 비교 타이밍 차이로 생길 수 있는 공격을 줄여줍니다.
    if not hmac.compare_digest(parts[2], expected_signature):
        raise TokenError("Invalid token")

    try:
        payload = json.loads(_base64url_decode(parts[1]).decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise TokenError("Invalid token") from None

    if int(payload.get("exp", 0)) < int(time.time()):
        raise TokenError("Token expired")

    # 토큰 payload의 sub에 들어 있는 사용자 id로 실제 Django User를 다시 찾습니다.
    user_id = payload.get("sub")
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        raise TokenError("Invalid token") from None
