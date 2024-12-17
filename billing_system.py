import razorpay
import psycopg2
import logging
from config import RAZORPAY_API_KEY, RAZORPAY_API_SECRET, DATABASE_URI

class BillingSystem:
    def __init__(self):
        # Initialize Razorpay client with your API credentials
        self.client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))

        # Initialize PostgreSQL database connection
        self.conn = psycopg2.connect(DATABASE_URI)
        self.cursor = self.conn.cursor()

    def process_billing(self):
        """Process Razorpay transactions and handle subscriptions."""
        logging.info("Processing billing...")

        try:
            # Example: Retrieve the list of payments to check for successful transactions
            payments = self.client.payment.all({'status': 'captured'})  # Retrieve successful payments
            if payments['items']:
                for payment in payments['items']:
                    logging.info(f"Payment ID: {payment['id']} - Amount: {payment['amount']} - Status: {payment['status']}")

            # Example: Verify subscription payment (if applicable)
            subscriptions = self.client.subscription.all({'status': 'active'})  # List active subscriptions
            for subscription in subscriptions['items']:
                logging.info(f"Subscription ID: {subscription['id']} - Amount: {subscription['amount_paid']} - Status: {subscription['status']}")

            logging.info("Billing processed successfully.")

        except razorpay.errors.RazorpayError as e:
            logging.error(f"Razorpay API error: {e}")
        except Exception as e:
            logging.error(f"Error processing billing: {e}")

    def create_order(self, amount, currency, payer):
        """
        Creates a Razorpay order and stores it in the database.
        :param amount: Amount to be paid
        :param currency: Currency for the payment (INR/USD)
        :param payer: The payer's name (Individual/Company)
        :return: Razorpay order details
        """
        order_data = {
            "amount": amount * 100,  # Razorpay requires amount in paise
            "currency": currency,
            "payment_capture": 1,
            "notes": {"payer": payer}
        }
        order = self.client.order.create(order_data)
        
        # Insert the order details into the database
        self.cursor.execute("""
            INSERT INTO payments (order_id, amount, currency, payer)
            VALUES (%s, %s, %s, %s)
        """, (order['id'], order['amount'], currency, payer))
        self.conn.commit()
        
        return order

    def verify_payment(self, order_id, payment_id, signature):
        """
        Verifies Razorpay payment signature.
        :param order_id: The order ID from Razorpay
        :param payment_id: The payment ID from Razorpay
        :param signature: The signature to be verified
        :return: True if verified, False otherwise
        """
        try:
            self.client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
            
            # Update payment status in the database
            self.cursor.execute("""
                UPDATE payments 
                SET payment_status = %s
                WHERE order_id = %s
            """, ('Success', order_id))
            self.conn.commit()
            
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

if __name__ == "__main__":
    # Example usage of the BillingSystem class
    logging.basicConfig(level=logging.INFO)
    billing_system = BillingSystem()

    # Example: Process billing transactions
    billing_system.process_billing()

    # Example: Create a new order
    order = billing_system.create_order(amount=500, currency="INR", payer="John Doe")
    logging.info(f"Created order: {order}")

    # Example: Verify payment (substitute with actual order, payment, and signature details)
    payment_verified = billing_system.verify_payment(order_id=order['id'], 
                                                    payment_id="payment_id_example", 
                                                    signature="signature_example")
    if payment_verified:
        logging.info("Payment verified successfully.")
    else:
        logging.error("Payment verification failed.")
