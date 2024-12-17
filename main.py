from flask import Flask, render_template, request, jsonify, redirect, url_for
from billing_system import BillingSystem
from bgp_simulator import BGPSimulator
from network_database import NetworkDatabase
from optimizer import NetworkOptimizer
from scheduler import add_network_data_task, cleanup_task
import schedule
import time
import threading

app = Flask(__name__)

# Initialize necessary systems
billing_system = BillingSystem()
bgp_simulator = BGPSimulator()
network_db = NetworkDatabase()
network_optimizer = NetworkOptimizer()

# Initialize scheduler tasks in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting

# Schedule tasks for network data addition and cleanup operations
schedule.every(15).minutes.do(add_network_data_task)
schedule.every().day.at("00:00").do(cleanup_task)

# Start the scheduler in a separate thread to run asynchronously with the Flask app
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # Daemonize the thread to stop it when the main app exits
scheduler_thread.start()

@app.route("/")
def index():
    # Render the main page for IXP management
    return render_template("index.html")

@app.route("/create_order", methods=["POST"])
def create_order():
    data = request.json
    amount = data["amount"]
    currency = data["currency"]
    payer = data["payer"]
    
    try:
        order = billing_system.create_order(amount, currency, payer)
        # Redirect to Razorpay checkout based on the selected currency
        if currency == "INR":
            payment_url = "https://rzp.io/rzp/JusDG4P"
        elif currency == "USD":
            payment_url = "https://rzp.io/rzp/BblrH9g9"
        else:
            return jsonify({"error": "Invalid currency selected"}), 400
        
        return jsonify({"order": order, "payment_url": payment_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/verify_payment", methods=["POST"])
def verify_payment():
    data = request.json
    order_id = data["order_id"]
    payment_id = data["payment_id"]
    signature = data["signature"]
    
    verified = billing_system.verify_payment(order_id, payment_id, signature)
    if verified:
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"}), 400

@app.route("/simulate_bgp", methods=["POST"])
def simulate_bgp():
    data = request.json
    network_data = data.get("network_data")
    result = bgp_simulator.simulate(network_data)
    return jsonify({"result": result})

@app.route("/optimize_network", methods=["POST"])
def optimize_network():
    data = request.json
    network_config = data.get("network_config")
    optimized_network = network_optimizer.optimize(network_config)
    return jsonify({"optimized_network": optimized_network})

@app.route("/add_network_data", methods=["POST"])
def add_network_data():
    data = request.json
    network_info = data.get("network_info")
    network_db.add_data(network_info)
    return jsonify({"status": "Network data added successfully"})

if __name__ == "__main__":
    app.run(debug=True)
