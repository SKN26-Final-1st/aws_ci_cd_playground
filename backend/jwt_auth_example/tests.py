from django.test import Client, TestCase


class JwtAuthExampleTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def login(self):
        response = self.client.post(
            "/api/jwt/login/",
            data={"username": "demo", "password": "demo1234"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        return response.json()["accessToken"]

    def test_login_returns_token_and_bearer_token_unlocks_protected_api(self):
        token = self.login()

        protected_response = self.client.get(
            "/api/jwt/protected/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(protected_response.status_code, 200)
        self.assertEqual(protected_response.json()["message"], "jwt secret")
        self.assertEqual(protected_response.json()["user"]["username"], "demo")

    def test_me_returns_user_for_valid_bearer_token(self):
        token = self.login()

        response = self.client.get(
            "/api/jwt/me/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["username"], "demo")

    def test_missing_bearer_token_is_rejected(self):
        response = self.client.get("/api/jwt/protected/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Bearer token required")

    def test_tampered_bearer_token_is_rejected(self):
        token = self.login()
        replacement = "a" if token[-1] != "a" else "b"
        tampered_token = f"{token[:-1]}{replacement}"

        response = self.client.get(
            "/api/jwt/protected/",
            HTTP_AUTHORIZATION=f"Bearer {tampered_token}",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Invalid token")
