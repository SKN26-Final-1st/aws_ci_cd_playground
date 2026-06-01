# Django React Auth Examples Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build runnable Django + React examples for basic API calls, session authentication, and JWT-style authentication.

**Architecture:** Django exposes three small plain-JSON apps under `/api/basic/`, `/api/session/`, and `/api/jwt/`. React uses a tabbed playground with focused components and a shared `fetch` helper.

**Tech Stack:** Django 6.0.5, SQLite, React 19, TypeScript, Vite, browser `fetch`.

---

## File Structure

- Create `backend/basic_api_example/`: public ping and echo endpoints plus tests.
- Create `backend/session_auth_example/`: demo-user helper, CSRF/session views, URLs, and tests.
- Create `backend/jwt_auth_example/`: minimal HS256 JWT helper, auth views, URLs, and tests.
- Modify `backend/backend/settings.py`: install apps, add dev CORS middleware, and configure local CSRF origins.
- Modify `backend/backend/urls.py`: include the three example URL modules.
- Create `backend/backend/cors.py`: local-only CORS headers for Vite dev server.
- Create `frontend/src/api.ts`: shared request helpers and response types.
- Create `frontend/src/examples/`: three focused React example components.
- Modify `frontend/src/App.tsx`, `frontend/src/App.css`, and `frontend/src/index.css`: replace the starter page with the playground.
- Create `docs/django-react-auth-examples.md`: run steps, endpoints, and auth-flow notes.

## Tasks

### Task 1: Backend Tests

**Files:**
- Create: `backend/basic_api_example/tests.py`
- Create: `backend/session_auth_example/tests.py`
- Create: `backend/jwt_auth_example/tests.py`

- [ ] Write tests for public ping and echo behavior.
- [ ] Write tests for session CSRF, login, protected access, logout, and denied protected access.
- [ ] Write tests for JWT login, protected access, missing-token denial, and tampered-token denial.
- [ ] Run `C:/Users/MIN/miniconda3/envs/web_service_env/python.exe manage.py test` from `backend/` and verify failures are caused by missing apps or routes.

### Task 2: Django API Implementation

**Files:**
- Create and modify the backend files listed in the file structure.

- [ ] Add `json_body`, `json_error`, and method guard helpers where they keep the examples readable.
- [ ] Implement basic API views and URLs.
- [ ] Implement demo-user creation with username `demo` and password `demo1234`.
- [ ] Implement session auth views with Django `authenticate`, `login`, and `logout`.
- [ ] Implement JWT signing, verification, expiration handling, and bearer-token parsing.
- [ ] Include app URLs under the project URLconf.
- [ ] Run backend tests until they pass.

### Task 3: React Playground

**Files:**
- Create: `frontend/src/api.ts`
- Create: `frontend/src/examples/BasicApiExample.tsx`
- Create: `frontend/src/examples/SessionAuthExample.tsx`
- Create: `frontend/src/examples/JwtAuthExample.tsx`
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/App.css`
- Modify: `frontend/src/index.css`

- [ ] Add shared request helpers that capture status, OK state, and JSON payload.
- [ ] Build the Basic API tab with ping and echo buttons.
- [ ] Build the Session Auth tab with CSRF, login, me, protected, and logout controls.
- [ ] Build the JWT Auth tab with login, me, protected, and token clear controls.
- [ ] Replace the Vite starter with the tabbed playground.
- [ ] Run TypeScript build once frontend dependencies are installed.

### Task 4: Documentation and Verification

**Files:**
- Create: `docs/django-react-auth-examples.md`
- Modify: `README.md` only if a short pointer is useful.

- [ ] Document backend and frontend run commands.
- [ ] List endpoints and demo credentials.
- [ ] Explain session-vs-JWT differences in this repo.
- [ ] Run backend tests.
- [ ] Run frontend build or report the missing dependency blocker.
