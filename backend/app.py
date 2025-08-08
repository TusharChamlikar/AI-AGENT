from flask import Flask, request, jsonify
from backend.scheduler.reminder_scheduler import start_scheduler
from backend.services.reminder_service import create_reminder  # import your service function
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

start_scheduler()

@app.route("/")
def home():
    return "PayMind AI Reminder Agent is running!"

# ✅ POST route for /reminders
@app.route("/reminders", methods=["POST"])
def add_reminder():
    data = request.get_json()

    # Extract required fields
    name = data.get("name")
    amount = data.get("amount")
    due_date = data.get("due_date")
    email= data.get("email")
    mobile = data.get("mobile")
    

    # Validate fields
    if not all([name, amount, due_date, email,mobile]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create reminder
    reminder = create_reminder(name, amount, due_date, email,mobile)
    return jsonify(reminder.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
