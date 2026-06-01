# Django + React 인증/API 통신 학습 예제

이 문서는 이 저장소에 추가된 Django + React 연결 예제를 학습하기 위한 안내서입니다.

목표는 “완성된 서비스 코드”를 만드는 것이 아니라, React 화면에서 버튼을 눌렀을 때 어떤 HTTP 요청이 Django로 가고, Django가 어떤 방식으로 로그인 상태나 토큰을 확인하는지 눈으로 따라가는 것입니다.

## 먼저 큰 그림부터 보기

이 예제는 세 가지 흐름을 분리해서 보여줍니다.

| 예제 | 핵심 질문 | React에서 보는 포인트 | Django에서 보는 포인트 |
| --- | --- | --- | --- |
| 기본 API | 로그인 없이 JSON을 주고받을 수 있나? | `fetch`, JSON body, 응답 상태 | `JsonResponse`, 요청 method, body 파싱 |
| 세션 인증 | Django 기본 로그인은 React와 어떻게 연결되나? | `credentials: 'include'`, CSRF 헤더 | `login`, `logout`, `request.user`, 세션 쿠키 |
| JWT 인증 | 쿠키 없이 토큰으로 인증하려면? | `Authorization: Bearer <token>` | 토큰 발급, 서명 검증, 보호 API |

추천 학습 순서:

1. 기본 API 탭에서 `GET`, `POST` 요청과 JSON 응답 모양을 익힙니다.
2. 세션 인증 탭에서 CSRF 토큰을 먼저 받고, 로그인 후 보호 API가 열리는 것을 확인합니다.
3. JWT 인증 탭에서 로그인 응답으로 받은 토큰이 보호 API 요청 헤더에 들어가는 흐름을 봅니다.

## 실행 방법

### 1. Django 백엔드 실행

처음 한 번은 마이그레이션을 실행해야 합니다.

```powershell
cd backend
C:/Users/MIN/miniconda3/envs/web_service_env/python.exe manage.py migrate
```

그 다음 개발 서버를 실행합니다.

```powershell
cd backend
C:/Users/MIN/miniconda3/envs/web_service_env/python.exe manage.py runserver 8000
```

일반 Python 환경을 쓰는 경우에는 먼저 의존성을 설치한 뒤 실행합니다.

```powershell
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

### 2. React 프론트엔드 실행

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

브라우저에서 Vite 주소를 엽니다.

```text
http://127.0.0.1:5173/
```

React가 호출하는 Django 주소는 기본값이 `http://localhost:8000`입니다. 다른 주소를 쓰고 싶다면 Vite 실행 전에 환경 변수를 지정합니다.

```powershell
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
npm.cmd run dev
```

## 데모 계정

로그인 API가 처음 호출될 때 Django 쪽에서 데모 사용자를 자동으로 준비합니다.

```text
username: demo
password: demo1234
```

관련 코드:

- [backend/backend/demo_users.py](../backend/backend/demo_users.py)

## 코드 위치

### Django

| 파일 | 역할 |
| --- | --- |
| [backend/backend/urls.py](../backend/backend/urls.py) | `/api/basic/`, `/api/session/`, `/api/jwt/` 라우팅 연결 |
| [backend/backend/api.py](../backend/backend/api.py) | JSON body 파싱, 공통 에러 응답 |
| [backend/backend/cors.py](../backend/backend/cors.py) | Vite 개발 서버에서 Django API를 호출할 수 있게 CORS 헤더 추가 |
| [backend/basic_api_example/views.py](../backend/basic_api_example/views.py) | 인증 없는 기본 API |
| [backend/session_auth_example/views.py](../backend/session_auth_example/views.py) | 세션 + CSRF 로그인 API |
| [backend/jwt_auth_example/views.py](../backend/jwt_auth_example/views.py) | JWT 방식 로그인/API |
| [backend/jwt_auth_example/tokens.py](../backend/jwt_auth_example/tokens.py) | 학습용 JWT 생성/검증 로직 |

### React

| 파일 | 역할 |
| --- | --- |
| [frontend/src/api.ts](../frontend/src/api.ts) | 공통 `fetch` helper, 쿠키 읽기 helper |
| [frontend/src/App.tsx](../frontend/src/App.tsx) | 탭 전환과 전체 학습 화면 |
| [frontend/src/examples/BasicApiExample.tsx](../frontend/src/examples/BasicApiExample.tsx) | 기본 API 호출 화면 |
| [frontend/src/examples/SessionAuthExample.tsx](../frontend/src/examples/SessionAuthExample.tsx) | 세션 인증 호출 화면 |
| [frontend/src/examples/JwtAuthExample.tsx](../frontend/src/examples/JwtAuthExample.tsx) | JWT 인증 호출 화면 |
| [frontend/src/examples/ResponsePanel.tsx](../frontend/src/examples/ResponsePanel.tsx) | 상태 코드와 JSON 응답 표시 |

## 기본 API 흐름

### GET `/api/basic/ping/`

React:

```ts
apiRequest('/api/basic/ping/')
```

Django:

```py
return JsonResponse({
    "ok": True,
    "message": "pong from Django",
    "method": request.method,
})
```

학습 포인트:

- 인증이 필요 없는 API는 쿠키나 토큰 없이 호출할 수 있습니다.
- React는 응답의 HTTP 상태 코드와 JSON body를 분리해서 확인하는 습관을 들이면 좋습니다.

### POST `/api/basic/echo/`

React:

```ts
apiRequest('/api/basic/echo/', {
  method: 'POST',
  body: { message, sentFrom: 'React' },
})
```

Django:

```py
data = parse_json_body(request)
return JsonResponse({"ok": True, "received": data})
```

학습 포인트:

- React가 `body`를 보내면 `Content-Type: application/json`이 필요합니다.
- Django 기본 `request.POST`는 form data 중심이므로, JSON body는 `request.body`에서 직접 읽거나 DRF 같은 도구를 씁니다.
- 이 예제에서는 학습을 위해 직접 `json.loads`로 파싱합니다.

## 세션 인증 흐름

세션 인증은 Django 기본 로그인 방식과 가장 가깝습니다. 핵심은 “로그인 상태를 서버 세션과 브라우저 쿠키가 함께 기억한다”는 점입니다.

### 전체 순서

1. React가 `GET /api/session/csrf/`를 호출합니다.
2. Django가 `csrftoken` 쿠키를 내려줍니다.
3. React가 로그인 요청에 `X-CSRFToken` 헤더와 JSON body를 함께 보냅니다.
4. Django가 `login(request, user)`를 실행하고 세션 쿠키를 내려줍니다.
5. 이후 React는 `credentials: 'include'`로 쿠키를 함께 보내 보호 API를 호출합니다.
6. Django는 `request.user.is_authenticated`로 로그인 여부를 확인합니다.

### 왜 `credentials: 'include'`가 필요한가?

React 개발 서버는 보통 `http://127.0.0.1:5173`, Django 서버는 `http://127.0.0.1:8000`입니다. 포트가 다르면 브라우저 입장에서는 서로 다른 출처입니다.

브라우저는 다른 출처로 `fetch`를 보낼 때 쿠키를 자동으로 포함하지 않습니다. 그래서 세션 쿠키를 Django에 보내려면 React 요청에 이 옵션이 필요합니다.

```ts
credentials: 'include'
```

### 왜 CSRF 토큰이 필요한가?

세션 인증은 쿠키를 사용합니다. 쿠키는 브라우저가 자동으로 붙일 수 있기 때문에, 악성 페이지가 사용자의 브라우저를 이용해 원치 않는 POST 요청을 보내는 위험이 있습니다.

Django는 이를 막기 위해 unsafe method인 `POST`, `PUT`, `PATCH`, `DELETE` 등에 CSRF 검사를 적용합니다. React에서는 쿠키에 있는 CSRF 토큰을 읽고 헤더로 다시 보내야 합니다.

```ts
headers: {
  'X-CSRFToken': csrfToken,
}
```

이 저장소의 React 코드는 로그인 후 CSRF 값이 바뀔 수 있는 상황도 고려해서, POST 요청 직전에 `csrftoken` 쿠키를 다시 읽습니다.

관련 코드:

- [frontend/src/examples/SessionAuthExample.tsx](../frontend/src/examples/SessionAuthExample.tsx)
- [frontend/src/api.ts](../frontend/src/api.ts)

### 세션 방식의 특징

장점:

- Django 기본 인증 기능과 잘 맞습니다.
- 서버가 세션을 관리하므로 로그아웃/세션 만료 처리가 직관적입니다.
- 브라우저 기반 웹앱에 자연스럽습니다.

주의할 점:

- CSRF 처리를 반드시 이해해야 합니다.
- 프론트와 백엔드 출처가 다르면 CORS와 쿠키 설정을 함께 봐야 합니다.
- 모바일 앱이나 외부 API 클라이언트까지 고려하면 토큰 방식이 더 편할 수 있습니다.

## JWT 인증 흐름

JWT 방식은 “로그인 상태를 쿠키 세션이 아니라 토큰으로 증명한다”는 방식입니다.

### 전체 순서

1. React가 `POST /api/jwt/login/`에 아이디/비밀번호를 보냅니다.
2. Django가 사용자 정보를 확인하고 access token을 발급합니다.
3. React가 token을 상태에 저장합니다.
4. 보호 API를 호출할 때 `Authorization` 헤더에 토큰을 넣습니다.
5. Django가 토큰 서명을 검증하고, 토큰 안의 사용자 정보를 바탕으로 요청을 허용합니다.

React 요청 예시:

```ts
apiRequest('/api/jwt/protected/', {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
})
```

Django 쪽 확인:

```py
authorization = request.headers.get("Authorization", "")
```

### 이 예제의 JWT는 왜 “학습용”인가?

[backend/jwt_auth_example/tokens.py](../backend/jwt_auth_example/tokens.py)는 JWT 구조를 이해하기 위한 최소 구현입니다.

여기서는 다음을 직접 보여줍니다.

- header와 payload를 base64url로 인코딩
- `SECRET_KEY`로 HMAC-SHA256 서명 생성
- 요청으로 받은 token의 서명 비교
- `exp` 만료 시간 확인

하지만 실제 서비스에서는 직접 구현하지 않는 편이 좋습니다. 운영 환경에서는 아래처럼 이미 검증된 패키지를 사용하세요.

- `djangorestframework`
- `djangorestframework-simplejwt`

실무에서는 추가로 고민해야 할 것이 많습니다.

- refresh token을 어떻게 발급/재발급할지
- access token 만료 시간을 얼마나 짧게 둘지
- 로그아웃 시 토큰을 어떻게 폐기할지
- 탈취된 토큰을 어떻게 막거나 회수할지
- 브라우저 저장 위치를 localStorage, memory, httpOnly cookie 중 어디로 할지

### JWT 방식의 특징

장점:

- 쿠키 세션에 덜 의존합니다.
- 모바일 앱, 외부 클라이언트, API 서버 구조와 잘 맞습니다.
- `Authorization` 헤더만 보면 인증 여부가 비교적 명확합니다.

주의할 점:

- 토큰 탈취 위험을 고려해야 합니다.
- 이미 발급된 토큰을 서버에서 즉시 무효화하기 어렵습니다.
- refresh token 설계가 들어가면 세션 방식보다 복잡해질 수 있습니다.

## 세션 인증과 JWT 인증 비교

| 관점 | 세션 인증 | JWT 인증 |
| --- | --- | --- |
| 로그인 상태 저장 | 서버 세션 + 브라우저 쿠키 | 클라이언트가 보관하는 토큰 |
| 요청에 붙는 값 | Cookie | `Authorization` 헤더 |
| CSRF 고려 | 필요 | 보통 Bearer 헤더 방식이면 상대적으로 덜 필요 |
| 로그아웃 | 서버 세션 삭제 | 클라이언트 토큰 삭제, 서버 블랙리스트는 별도 설계 |
| Django 기본 기능과 궁합 | 좋음 | DRF/SimpleJWT 조합이 일반적 |
| 학습 난이도 | CSRF 때문에 초반에 헷갈릴 수 있음 | 토큰 저장/만료/갱신에서 복잡해짐 |

## CORS는 왜 필요한가?

개발 중에는 React와 Django가 서로 다른 포트에서 실행됩니다.

```text
React: http://127.0.0.1:5173
Django: http://127.0.0.1:8000
```

브라우저는 다른 출처로 API 요청을 보낼 때 CORS 정책을 확인합니다. 이 저장소는 학습용으로 [backend/backend/cors.py](../backend/backend/cors.py)에 작은 개발용 CORS middleware를 두었습니다.

허용하는 개발 출처:

```py
DEV_ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}
```

실제 프로젝트에서는 직접 middleware를 만들기보다 `django-cors-headers` 같은 패키지를 쓰는 편이 일반적입니다.

## 자주 막히는 부분

### 403 CSRF verification failed

세션 로그인이나 로그아웃 POST에서 자주 봅니다.

확인할 것:

- 먼저 `/api/session/csrf/`를 호출했는지
- `credentials: 'include'`를 넣었는지
- `X-CSRFToken` 헤더가 들어갔는지
- 로그인 후 CSRF 쿠키가 바뀌었을 때 최신 쿠키를 읽고 있는지

### 401 Bearer token required

JWT 보호 API에서 토큰 없이 호출했을 때 나옵니다.

확인할 것:

- `/api/jwt/login/`을 먼저 호출했는지
- 응답의 `accessToken`을 저장했는지
- 요청 헤더가 정확히 `Authorization: Bearer <token>` 형태인지

### 프론트에서 Network Error가 보일 때

확인할 것:

- Django 서버가 `8000` 포트에서 실행 중인지
- Vite 서버가 `5173` 포트에서 실행 중인지
- `VITE_API_BASE_URL` 값이 맞는지
- 브라우저 개발자 도구 Console/Network 탭에 CORS 에러가 있는지

## 테스트와 검증

백엔드 테스트:

```powershell
cd backend
C:/Users/MIN/miniconda3/envs/web_service_env/python.exe manage.py test basic_api_example session_auth_example jwt_auth_example
```

프론트엔드 린트:

```powershell
cd frontend
npm.cmd run lint
```

프론트엔드 빌드:

```powershell
cd frontend
npm.cmd run build
```

## 다음에 확장해볼 만한 것

이 예제가 익숙해지면 다음 순서로 확장해보면 좋습니다.

1. 회원가입 API 추가
2. 로그인 실패 횟수 제한
3. JWT refresh token 예제 추가
4. React Context로 로그인 상태 전역 관리
5. React Router로 공개 페이지/보호 페이지 분리
6. DRF + SimpleJWT 버전으로 같은 예제 다시 만들기
