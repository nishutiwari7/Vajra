import unittest
from app import app

class TestUIService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200, "Index page should load successfully")

    def test_create_order(self):
        response = self.app.post(
            "/create_order",
            json={"amount": 100, "currency": "INR", "payer": "User1"},
        )
        self.assertEqual(response.status_code, 200, "Order creation should succeed")
        self.assertIn("id", response.json, "Order response should contain an ID")

    def test_verify_payment(self):
        response = self.app.post(
            "/verify_payment",
            json={"order_id": "order_123", "payment_id": "pay_456", "signature": "test_signature"},
        )
        self.assertEqual(response.status_code, 200, "Payment verification should succeed")
        self.assertEqual(response.json["status"], "success", "Payment should be verified")
