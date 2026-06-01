# Django React Auth Examples Design

## Goal

Add small, runnable Django and React examples that show three separate connection patterns:

- Basic unauthenticated API calls
- Django session authentication with CSRF and cookies
- JWT-style bearer token authentication

The examples are for learning and comparison, not production hardening.

## Architecture

The Django backend exposes plain JSON endpoints without Django REST Framework so the HTTP mechanics stay visible. Three small apps keep the examples separate:

- `basic_api_example` owns public request/response examples.
- `session_auth_example` owns cookie session login, logout, current-user, and protected-resource endpoints.
- `jwt_auth_example` owns demo bearer-token login, current-user, and protected-resource endpoints.

The React frontend replaces the Vite starter with a compact tabbed playground. Each tab calls one backend flow with `fetch`, displays the endpoint being exercised, and renders the JSON response or error.

## Backend Behavior

### Basic API

- `GET /api/basic/ping/` returns an OK message and HTTP method.
- `POST /api/basic/echo/` returns the JSON body sent by the client.

### Session Auth

- `GET /api/session/csrf/` sets the CSRF cookie and returns the cookie name expected by Django.
- `POST /api/session/login/` accepts `username` and `password`, validates a demo user, and creates a Django session.
- `POST /api/session/logout/` clears the Django session.
- `GET /api/session/me/` returns the authenticated user or an anonymous state.
- `GET /api/session/protected/` returns protected demo data only for authenticated session users.

React must call session endpoints with `credentials: "include"` and send `X-CSRFToken` on unsafe requests.

### JWT-Style Auth

- `POST /api/jwt/login/` accepts the same demo credentials and returns an access token.
- `GET /api/jwt/me/` reads the bearer token and returns the user.
- `GET /api/jwt/protected/` returns protected demo data only when `Authorization: Bearer <token>` is valid.

The token implementation uses a small HS256 JWT helper built with the Python standard library. The code and docs must clearly say this is educational and that production Django APIs should use a maintained package such as `djangorestframework-simplejwt`.

## Frontend Behavior

The first screen is the working playground, not a marketing page. It includes:

- Tabs for Basic API, Session Auth, and JWT Auth.
- Login forms prefilled with `demo` / `demo1234`.
- Buttons for each request in the flow.
- A response panel showing status and JSON payload.

The UI uses plain React state and `fetch`; no routing, axios, or global state library is added.

## Error Handling

Backend endpoints return JSON errors with these status codes:

- `400` for invalid JSON or missing credentials.
- `401` for invalid login or invalid bearer token.
- `403` for protected session resources when unauthenticated.
- `405` when an endpoint receives an unsupported method.

Frontend request helpers surface both successful JSON and error JSON in the response panel.

## Testing

Backend tests cover:

- Basic `ping` and `echo` endpoints.
- Session CSRF cookie creation, login, protected access, logout, and denied protected access after logout.
- JWT login, protected access with a valid token, missing-token denial, and tampered-token denial.

Frontend verification uses TypeScript build once dependencies are available.

## Documentation

Add a short docs page explaining:

- How to run Django and React locally.
- Which endpoints belong to each example.
- The difference between session auth and JWT auth in this playground.
- The demo credentials.
