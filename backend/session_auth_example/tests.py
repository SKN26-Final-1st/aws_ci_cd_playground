from django.conf import settings
from django.test import Client, TestCase


class SessionAuthExampleTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def csrf_token(self):
        response = self.client.get("/api/session/csrf/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(settings.CSRF_COOKIE_NAME, response.cookies)
        return response.cookies[settings.CSRF_COOKIE_NAME].value

    def test_csrf_endpoint_sets_cookie(self):
        token = self.csrf_token()

        self.assertTrue(token)

    def test_login_me_protected_and_logout_flow(self):
        token = self.csrf_token()

        login_response = self.client.post(
            "/api/session/login/",
            data={"username": "demo", "password": "demo1234"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()["user"]["username"], "demo")

        me_response = self.client.get("/api/session/me/")
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()["user"]["username"], "demo")

        protected_response = self.client.get("/api/session/protected/")
        self.assertEqual(protected_response.status_code, 200)
        self.assertEqual(protected_response.json()["message"], "session secret")

        rotated_token = self.client.cookies[settings.CSRF_COOKIE_NAME].value
        logout_response = self.client.post(
            "/api/session/logout/",
            data={},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=rotated_token,
        )
        self.assertEqual(logout_response.status_code, 200)

        denied_response = self.client.get("/api/session/protected/")
        self.assertEqual(denied_response.status_code, 403)
        self.assertEqual(denied_response.json()["error"], "Authentication required")

    def test_login_rejects_bad_credentials(self):
        token = self.csrf_token()

        response = self.client.post(
            "/api/session/login/",
            data={"username": "demo", "password": "wrong"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Invalid credentials")
