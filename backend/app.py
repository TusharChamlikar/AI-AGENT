from flask import Flask, request, jsonify
from backend.scheduler.reminder_scheduler import start_scheduler
from backend.services.reminder_service import create_reminder  # import your service function

app = Flask(__name__)
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
    contact = data.get("contact")

    # Validate fields
    if not all([name, amount, due_date, contact]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create reminder
    reminder = create_reminder(name, amount, due_date, contact)
    return jsonify(reminder.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
