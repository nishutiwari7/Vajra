from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import razorpay
from config import RAZORPAY_API_KEY, RAZORPAY_API_SECRET, PAYMENT_LINKS, DATABASE_URI
from ixp_manager import IXPManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

razorpay_client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
ixp_manager = IXPManager()

# Database Models
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class NetworkActivity(db.Model):
    __tablename__ = 'network_activity'
    id = db.Column(db.Integer, primary_key=True)
    network_name = db.Column(db.String(100), nullable=False)
    data_usage = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Routes
@app.route("/")
def index():
    return render_template("index.html", payment_links=PAYMENT_LINKS)

@app.route("/ixp_status", methods=["GET"])
def get_ixp_status():
    ixp_list = request.args.getlist("ixp_list")
    ixp_manager.monitor_ixps(ixp_list)
    return jsonify(ixp_manager.ixp_status)

@app.route("/analytics", methods=["GET"])
def analytics_dashboard():
    # Fetch data from the database
    total_revenue = db.session.query(db.func.sum(Payment.amount)).scalar()
    total_users = db.session.query(User).count()
    network_usage = db.session.query(NetworkActivity.network_name, db.func.sum(NetworkActivity.data_usage)) \
                              .group_by(NetworkActivity.network_name).all()

    # Format data for JSON response
    response_data = {
        "total_revenue": total_revenue or 0,
        "total_users": total_users,
        "network_usage": {row[0]: row[1] for row in network_usage}
    }
    return jsonify(response_data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

    app.run(debug=True)
