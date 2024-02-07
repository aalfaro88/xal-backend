import unittest
from main import app


class TestStackExchangeRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_stackexchange_route(self):
        response = self.app.get("/stackexchange/stackexchange")
        self.assertEqual(response.status_code, 200)

    def test_answered_unanswered_route(self):
        response = self.app.get("/stackexchange/answered-unanswered")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("answered" in data)
        self.assertTrue("unanswered" in data)

    def test_highest_reputation_route(self):
        response = self.app.get("/stackexchange/highest-reputation")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("owner" in data)
        self.assertTrue("reputation" in data["owner"])

    def test_fewest_views_route(self):
        response = self.app.get("/stackexchange/fewest-views")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("view_count" in data)

    def test_oldest_recent_route(self):
        response = self.app.get("/stackexchange/oldest-recent")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("oldest" in data)
        self.assertTrue("most_recent" in data)


if __name__ == "__main__":
    unittest.main()
