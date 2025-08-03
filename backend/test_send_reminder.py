import os
from datetime import date
from dotenv import load_dotenv
from backend.utils.send_reminder import send_reminder
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import requests

# Load environment variables
load_dotenv()

# Mock Reminder class
class Reminder:
    def __init__(self, name, amount, due_date, contact):
        self.name = name
        self.amount = amount
        self.due_date = due_date
        self.contact = contact

# Create test reminders
reminder_email = Reminder(
    name="Tushar",
    amount=8500,
    due_date=date.today().isoformat(),
    contact="chamlikartushar@gmail.com"
)

reminder_sms = Reminder(
    name="Tushar",
    amount=8500,
    due_date=date.today().isoformat(),
    contact="+918839382885"
)

# === Run tests ===
print("\n=== Testing Email Reminder ===")
send_reminder(reminder_email)

print("\n=== Testing SMS Reminder ===")
send_reminder(reminder_sms)

# === Voice Reminder Test: Send MP3 via Email ===
def send_voice_attachment_email(reminder):
    mp3_path = f"{reminder.name}_reminder.mp3"
    if not os.path.exists(mp3_path):
        print("⚠️ MP3 not found, skipping voice attachment email.")
        return

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        from_email = os.getenv("FROM_EMAIL")
        to_email = reminder.contact

        with open(mp3_path, "rb") as f:
            data = f.read()
            encoded_file = base64.b64encode(data).decode()

        attached_file = Attachment(
            FileContent(encoded_file),
            FileName(f"{reminder.name}_reminder.mp3"),
            FileType("audio/mpeg"),
            Disposition("attachment")
        )

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject="🔊 Voice Reminder: Your Payment is Due",
            html_content=f"""
                <p>Hi {reminder.name},</p>
                <p>Attached is your voice reminder for payment of ₹{reminder.amount} due on {reminder.due_date}.</p>
                <p>— PayMind AI</p>
            """
        )
        message.attachment = attached_file

        sg.send(message)
        print(f"📧 Voice reminder sent with MP3 attached to {to_email}")
    except Exception as e:
        print(f"❌ Error sending voice reminder email: {e}")

print("\n=== Sending Voice Reminder MP3 via Email ===")
send_voice_attachment_email(reminder_email)

# === Voice Call via Retell AI ===
def send_retell_call(reminder):
    if not reminder.contact.startswith("+"):
        print("⚠️ Retell AI skipped: invalid phone number")
        return

    url = "https://api.retellai.com/v1/call"  # ✅ Correct endpoint
    headers = {
        "Authorization": f"Bearer {os.getenv('RETELL_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent_id": os.getenv("RETELL_AGENT_ID"),
        "phone_number": reminder.contact
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"📞 Retell AI call initiated to {reminder.contact}")
    else:
        print(f"❌ Retell API Error: {response.status_code} — {response.text}")