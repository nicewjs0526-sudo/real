from django.test import TestCase


class CoreViewsTests(TestCase):
    def test_home_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "REAL")

    def test_status_reports_database(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["app"], "ok")
        self.assertEqual(payload["database"], "ok")

