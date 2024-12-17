import unittest
from billing_system import BillingSystem

class TestBillingSystem(unittest.TestCase):
    def setUp(self):
        self.billing_system = BillingSystem()

    def test_create_order_inr(self):
        order = self.billing_system.create_order(amount=100, currency="INR", payer="User1")
        self.assertIn("id", order, "Order should contain an ID")
        self.assertEqual(order["currency"], "INR", "Order currency should be INR")

    def test_create_order_usd(self):
        order = self.billing_system.create_order(amount=10, currency="USD", payer="User1")
        self.assertIn("id", order, "Order should contain an ID")
        self.assertEqual(order["currency"], "USD", "Order currency should be USD")

    def test_verify_payment(self):
        # Mock data
        order_id = "order_123"
        payment_id = "pay_456"
        signature = "test_signature"

        verified = self.billing_system.verify_payment(order_id, payment_id, signature)
        self.assertTrue(verified, "Payment verification should succeed")
