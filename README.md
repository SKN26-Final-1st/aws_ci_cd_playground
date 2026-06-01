# react_ts_playground

**SKN26 파이널 프로젝트**를 앞두고 **React + TypeScript**와 **Django API 연동**을 익히기 위한 개인 연습 저장소입니다.

지금은 단순 프론트 연습을 넘어, **React 화면에서 버튼을 누르면 Django API로 어떤 HTTP 요청이 가고, 서버가 로그인/인증을 어떻게 처리하는지** 눈으로 따라가는 작은 풀스택 학습 사이트로 발전했습니다.

---

## 이게 무슨 사이트인가

React(프론트) + Django(백엔드)로 만든 **인증·API 통신 학습용 데모 사이트**입니다.  
화면 상단의 탭을 누르면서 요청 URL, 상태 코드, JSON 응답, 쿠키/토큰 변화를 직접 확인할 수 있습니다.

세 가지 흐름을 분리해서 보여줍니다.

| 탭 | 핵심 질문 | React에서 보는 것 | Django에서 보는 것 |
|------|-----------|------------------|--------------------|
| **기본 API** | 로그인 없이 JSON을 주고받을 수 있나? | `fetch`, JSON body, 응답 상태 | `JsonResponse`, 요청 method, body 파싱 |
| **세션 인증** | Django 기본 로그인은 React와 어떻게 연결되나? | `credentials: 'include'`, CSRF 헤더 | `login` / `logout`, `request.user`, 세션 쿠키 |
| **JWT 인증** | 쿠키 없이 토큰으로 인증하려면? | `Authorization: Bearer <token>` | 토큰 발급, 서명 검증, 보호 API |

추천 학습 순서: **기본 API → 세션 인증 → JWT 인증**

> 인증/통신 흐름에 대한 더 자세한 설명은 [docs/django-react-auth-examples.md](docs/django-react-auth-examples.md)를 참고하세요.

---

## 화면에서 볼 수 있는 것

- 탭별 데모 화면 (기본 API / 세션 인증 / JWT 인증)
- 요청을 보낼 때마다 표시되는 **요청 URL · HTTP 상태 코드 · JSON 응답** 패널
- 세션 로그인 시 CSRF 토큰을 먼저 받고 → 로그인 → 보호 API가 열리는 과정
- JWT 로그인 응답으로 받은 토큰이 보호 API 요청 헤더에 들어가는 과정

데모 로그인 계정:

```text
username: demo
password: demo1234
```

(로그인 API가 처음 호출될 때 Django가 데모 사용자를 자동으로 만들어 둡니다.)

---

## 왜 이 저장소를 만들었나

[4차 프로젝트 (LGneer)](https://github.com/SKN26-4th-1st/4th_project)에서는 아래 스택으로 프론트를 구현했습니다.

| 구분 | 4차 프로젝트 |
|------|----------------|
| 렌더링 | Django Templates (SSR) |
| 스타일 | Tailwind CSS v4, DaisyUI |
| 동작 | 바닐라 JavaScript (`static/js/`) |
| 구조 | `templates/` + `components/` 부분 템플릿 |

검색·필터·탭·챗봇·로그인 패널처럼 **화면이 복잡해질수록** HTML 조각과 JS가 함께 늘어나고, “어디서 이 UI가 갱신되는지”를 추적하는 비용이 커졌습니다.  
파이널에서는 백엔드(API)와 프론트(UI)를 더 분리하고, UI 복잡도를 React 쪽에서 다루는 연습을 이 repo에서 합니다.

---

## Django 템플릿 + HTML/JS vs React — 무엇이 달라지나

4차 방식도 **충분히 좋은 선택**이었습니다. Django SSR + Tailwind로 빠르게 실사용 UI를 만들 수 있었고, 팀이 익숙한 HTML/CSS/JS만으로도 디테일한 화면(필터 유지, 탭 전환, 가격 포맷 등)을 구현했습니다.

다만 **기능·화면·상태가 커질 때** React(와 TypeScript)가 주는 이점이 분명해집니다.

### 1. UI를 “문자열 조각”이 아니라 “컴포넌트”로 다룸

4차에서는 비슷한 카드·버튼·필터 UI가 여러 템플릿에 흩어지고, `{% include %}`와 JS가 같은 요소를 각각 건드리는 식으로 맞춰야 했습니다.

React에서는 **한 번 만든 컴포넌트**를 props만 바꿔 재사용합니다. 디자인 수정 시 파일 한곳을 고치면 되고, “이 버튼이 어느 페이지 JS에 묶여 있지?” 같은 추적이 줄어듭니다.

### 2. 명령형 DOM 조작 → 선언형 UI

바닐라 JS는 대략 이런 흐름입니다.

- DOM을 찾고 → 클래스/텍스트를 바꾸고 → 이벤트를 다시 붙인다.

상태가 여러 파일·여러 함수에 나뉘면 **UI와 데이터가 어긋나기** 쉽습니다(필터는 A인데 목록만 B로 그려짐 등).

React는 **상태(state)가 바뀌면 화면이 그 상태에 맞게 다시 그려진다**고 생각하면 됩니다. “지금 검색어·페이지·로딩 여부가 뭐지?”를 한곳에서 보고, 그에 맞는 JSX를 쓰면 됩니다.

### 3. 프론트와 백엔드 역할 분리

Django 템플릿은 **서버가 HTML을 완성해서 내려주는** 모델에 강합니다.  
반면 검색 결과 무한 스크롤, 실시간 채팅 UI, 클라이언트만의 폼 검증·낙관적 업데이트처럼 **브라우저에서 자주 바뀌는 UI**는 API(JSON) + SPA(또는 하이브리드)가 다루기 편합니다.

4차에서도 `fetch`로 API를 호출했지만, **화면 골격은 서버 템플릿**, **일부 동작만 JS**라 경계가 흐릴 수 있습니다.  
React 앱은 “UI 전담 클라이언트”로 두고 Django/FastAPI 등은 **REST·JSON API**에 집중하는 구조로 가기 쉽습니다 — 파이널 아키텍처 연습에 맞습니다. (이 repo의 백엔드/프론트 분리가 바로 그 연습입니다.)

### 4. TypeScript로 계약을 코드에 남김

4차의 JS는 런타임에야 타입·필드 오류를 알 수 있는 경우가 많았습니다.

TypeScript는 **API 응답 형태, props, 전역 상태**를 미리 정의해 두어, 잘못된 필드 접근·null 처리 누락을 **작성 단계에서** 잡는 데 유리합니다. 팀 규모가 커지거나 API 스펙이 자주 바뀔수록 체감이 큽니다.

### 5. 생태계와 도구

Vite(HMR), React DevTools, ESLint, 컴포넌트 단위 스토리/테스트 등 **프론트 전용 워크플로**가 잘 갖춰져 있습니다.  
Tailwind는 React와도 그대로 같이 쓸 수 있어, 4차에서 익힌 스타일링 감각은 **그대로 이어가면** 됩니다.

### 정리 — 4차 스택이 나쁜 게 아니라, “규모”에 맞는 선택

| 관점 | Django Template + HTML/JS | React + TypeScript |
|------|---------------------------|---------------------|
| 적합한 경우 | 페이지 수 적음, SEO·SSR 중요, 서버 중심 CRUD | 화면·상태·상호작용이 많음, API 기반 UI |
| UI 재사용 | include/복사 + JS 이벤트 연결 | 컴포넌트 + props |
| 상태 관리 | DOM + 전역 변수/파일 분산 | 컴포넌트 state, Context, 외부 store |
| 백엔드 연동 | context + 템플릿 + 가끔 fetch | fetch/axios + 명확한 API 타입 |
| 학습 목표 (이 repo) | — | 파이널 프론트 구조 연습 |

---

## 기술 스택

| 영역 | 사용 기술 |
|------|-----------|
| 프론트엔드 | React 19, TypeScript, Vite |
| 백엔드 | Django 6 (학습용 순수 함수 view + JSON 응답) |
| 인증 예제 | 세션 + CSRF, 학습용 JWT(직접 구현) |

> 백엔드는 학습 목적이라 DRF 없이 Django 기본 기능만으로 JSON API를 직접 만들었습니다. 실무에서는 `djangorestframework`, `djangorestframework-simplejwt`, `django-cors-headers` 사용을 권장합니다.

---

## 프로젝트 구조

```
react_ts_playground/
├── README.md              # 이 문서
├── docs/                  # 인증/API 흐름 상세 설명 문서
│   └── django-react-auth-examples.md
├── backend/               # Django API 서버
│   ├── manage.py
│   ├── requirements.txt
│   ├── backend/           # 설정, 라우팅, 공통 API/CORS helper, 데모 계정
│   ├── basic_api_example/      # 인증 없는 기본 API
│   ├── session_auth_example/   # 세션 + CSRF 로그인 API
│   └── jwt_auth_example/       # JWT 로그인/보호 API
└── frontend/              # Vite + React 19 + TypeScript
    ├── src/
    │   ├── App.tsx             # 탭 전환 + 전체 학습 화면
    │   ├── api.ts              # 공통 fetch helper, 쿠키 읽기 helper
    │   └── examples/           # 탭별 데모 컴포넌트
    ├── public/
    └── package.json
```

---

## 클론 받고 실행하기

### 0. 사전 준비물

- **Git**
- **Node.js 18+** (프론트엔드, npm 포함)
- **Python 3.12+** (백엔드, Django 6)

### 1. 저장소 클론

```bash
git clone https://github.com/SKN26-Final-1st/react_ts_playground.git
cd react_ts_playground
```

### 2. 백엔드(Django) 실행

```bash
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

> Django 서버는 `http://localhost:8000`에서 실행됩니다.

### 3. 프론트엔드(React) 실행

새 터미널을 열어 진행합니다.

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 Vite가 안내하는 주소(보통 `http://localhost:5173`)로 접속합니다.

> React가 호출하는 API 주소 기본값은 `http://localhost:8000`입니다. 다른 주소를 쓰려면 Vite 실행 전에 환경 변수 `VITE_API_BASE_URL`을 지정하세요.

### 자주 쓰는 명령

프론트엔드 (`frontend/`):

| 명령 | 설명 |
|------|------|
| `npm run dev` | 개발 서버 (HMR) |
| `npm run build` | 타입 체크 + 프로덕션 빌드 |
| `npm run preview` | 빌드 결과 미리보기 |
| `npm run lint` | ESLint |

백엔드 (`backend/`):

| 명령 | 설명 |
|------|------|
| `python manage.py runserver 8000` | 개발 서버 |
| `python manage.py migrate` | DB 마이그레이션 |
| `python manage.py test` | 인증/API 예제 테스트 |

---

## 이 playground에서 연습할 것

- 함수형 컴포넌트, `useState` / `useEffect` / 커스텀 훅
- props·children, 조건부/목록 렌더링
- 폼 입력, 로딩·에러 UI
- `fetch`로 JSON API 호출 (Django API와 통신)
- 세션/CSRF, JWT 등 **인증·인가 흐름** 직접 따라가기
- TypeScript: `interface`, 제네릭, API 응답 타입
- (추후) React Router, Context/Zustand, Tailwind 재도입

작은 실험은 `frontend/src/` 아래에 파일을 추가하거나 `App.tsx`를 바꿔가며 진행하면 됩니다.

---

## 참고 링크

- [인증/API 학습 상세 문서](docs/django-react-auth-examples.md) — 흐름·코드 위치·트러블슈팅
- [4차 프로젝트 저장소](https://github.com/SKN26-4th-1st/4th_project) — Django + LangGraph + 템플릿 기반 UI
- [React 공식 문서](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Django 공식 문서](https://docs.djangoproject.com/)

---

**서민혁** — 파이널 전 React/TS · Django API 워밍업
