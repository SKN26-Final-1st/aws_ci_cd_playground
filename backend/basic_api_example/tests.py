from django.test import Client, TestCase


class BasicApiExampleTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_ping_returns_public_django_response(self):
        response = self.client.get("/api/basic/ping/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "ok": True,
                "message": "pong from Django",
                "method": "GET",
            },
        )

    def test_echo_returns_posted_json_body(self):
        response = self.client.post(
            "/api/basic/echo/",
            data={"message": "hello React", "count": 1},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "ok": True,
                "received": {"message": "hello React", "count": 1},
            },
        )
