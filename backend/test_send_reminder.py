import os
from datetime import date
from dotenv import load_dotenv
from backend.utils.send_reminder import send_reminder

# Load environment variables from .env file
load_dotenv()

# Mock Reminder class to simulate your database model
class Reminder:
    def __init__(self, name, amount, due_date, contact):
        self.name = name
        self.amount = amount
        self.due_date = due_date
        self.contact = contact

# --- Test Email Reminder ---
reminder_email = Reminder(
    name="Tushar",
    amount=8500,
    due_date=date.today().isoformat(),
    contact="vishwas7782@gmail.com"  # Replace with your test email
)

# --- Test SMS Reminder ---
reminder_sms = Reminder(
    name="Tushar",
    amount=8500,
    due_date=date.today().isoformat(),
    contact="+918839382885"  # Replace with your Twilio verified test phone number
)

# Run Email test
print("\n=== Testing Email Reminder ===")
send_reminder(reminder_email)

# Run SMS test
print("\n=== Testing SMS Reminder ===")
send_reminder(reminder_sms)
