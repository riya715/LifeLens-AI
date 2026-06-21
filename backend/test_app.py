import unittest
from io import BytesIO

from backend.app import app, create_app


class TestLifeLensApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("LifeLens AI", response.get_data(as_text=True))

    def test_analyze_route_accepts_journal(self):
        response = self.client.post(
            "/analyze",
            data={"journal": "Today was productive."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Today was productive.", response.get_data(as_text=True))

    def test_upload_route_renders_analysis_page(self):
        response = self.client.post(
            "/upload",
            data={
                "journal_file": (
                    BytesIO(b"Today I was excited and studied for hours."),
                    "journal.txt",
                )
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("LifeLens AI", response.get_data(as_text=True))
        self.assertIn("Positive 😊", response.get_data(as_text=True))
        self.assertIn("High 🚀", response.get_data(as_text=True))

    def test_create_app_returns_flask_app(self):
        created_app = create_app()
        self.assertIsNotNone(created_app)


if __name__ == "__main__":
    unittest.main()
