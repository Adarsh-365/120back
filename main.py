from database.base import  Persistance
from model import Data
from dotenv import load_dotenv
import os
from datetime import  datetime
import os
import os
import razorpay
load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
TABLE_NAME = os.getenv("TABLE_NAME", "users")


from payment.razorpay import client
from flask import Flask, jsonify , request

app = Flask(__name__)

from flask_cors import CORS

db = Persistance()

# app = Flask(__name__)
CORS(app, origins=[ "*"])
@app.route("/")
def home():
    return "Hello, World!"


@app.route("/about")
def about():
    return {
        "name": "Adarsh",
        "framework": "Flask"
    }


@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        # Convert cost to integer (Razorpay expects amount in paise as an integer)
        amount_str = os.environ.get("COURCE_COST")
        if not amount_str:
            raise ValueError("COURCE_COST environment variable is not set")
        amount = int(amount_str)

        order = client.order.create({
            "amount": amount,  # amount in paise
            "currency": "INR",
            "receipt": "order_001"
        })
        
        return jsonify({
            "order_id": order["id"],
            "key": RAZORPAY_KEY_ID,
            "amount": order["amount"],
            "currency": order["currency"]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.post("/verify-payment")
def verify_payment():
    data = request.json
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
        
        # Prepare data for database
        enrollment_data = {
            "payment_id": data["razorpay_payment_id"],
            "order_id": data["razorpay_order_id"],
            "name": data["formData"]["name"],
            "mobile": data["formData"]["mobile"],
            "email": data["formData"]["email"],
            "city": data["formData"]["city"],
            "state": data["formData"]["state"],
            "country": data["formData"]["country"],
            "course": data["formData"]["course"],
            "message": data["formData"]["message"],
            "payment_status": "completed",
            "timestamp": str(datetime.now().isoformat())
        }
        
        # Save to database
        db.insert(tabel=TABLE_NAME,data=enrollment_data)
        
        return jsonify({
            "success": True,
            "message": "Payment verified successfully.",
            "payment_id": data["razorpay_payment_id"],
            "order_id": data["razorpay_order_id"]
        })
    except razorpay.errors.SignatureVerificationError:
        return jsonify({
            "success": False,
            "message": "Invalid payment signature."
        }), 400


from flask import Flask, request, jsonify
from functools import wraps
import os

# Admin credentials
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME" )
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
            return jsonify({
                "success": False,
                "message": "Authentication required"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# Get all enrollments - Admin only
@app.route("/admin/enrollments", methods=["GET"])
@require_auth
def get_all_enrollments():
    try:
        # Use the correct method based on your Persistance library
        # Option 1: If using select_all()
        columns, rows = db.get_all(TABLE_NAME)
        print("Columns:", columns)
        print("Rows count:", len(rows))
        
        # Format the data
        enrollment_list = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            enrollment_list.append({
                "id": row_dict.get("id"),
                "payment_id": row_dict.get("payment_id"),
                "order_id": row_dict.get("order_id"),
                "name": row_dict.get("name"),
                "mobile": row_dict.get("mobile"),
                "email": row_dict.get("email"),
                "city": row_dict.get("city"),
                "state": row_dict.get("state"),
                "country": row_dict.get("country"),
                "course": row_dict.get("course"),
                "message": row_dict.get("message"),
                "payment_status": row_dict.get("payment_status"),
                "timestamp": str(row_dict.get("timestamp")) if row_dict.get("timestamp") is not None else None
            })
        
        return jsonify({
            "success": True,
            "count": len(enrollment_list),
            "data": enrollment_list
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


        
        
if __name__ == "__main__":
    app.run(debug=True)


# data = Data(first_name="pragati",middle_name="vishnu",sirname="tayde",mob_no="443201",city="mumbai")
# data_dict = data.model_dump()
# print(data_dict)


# db = Persistance()

# table = "members"

# db.insert(table,data_dict)