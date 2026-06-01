from django.contrib.auth import authenticate, get_user_model


DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


def ensure_demo_user():
    # 예제를 바로 실행할 수 있도록 demo 계정을 필요할 때 자동으로 준비합니다.
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={"email": "demo@example.com", "first_name": "Demo"},
    )

    if created or not user.check_password(DEMO_PASSWORD):
        # 비밀번호가 바뀌었거나 처음 만든 경우에도 항상 문서의 demo1234로 맞춥니다.
        user.set_password(DEMO_PASSWORD)
        user.save(update_fields=["password"])

    return user


def authenticate_demo_user(request, username, password):
    # authenticate는 DB에 사용자가 있어야 하므로 먼저 demo 계정을 보장합니다.
    ensure_demo_user()
    return authenticate(request, username=username, password=password)


def serialize_user(user):
    # Django User 객체 전체를 노출하지 않고 화면 학습에 필요한 값만 JSON으로 보냅니다.
    return {
        "id": user.id,
        "username": user.get_username(),
        "email": user.email,
    }
