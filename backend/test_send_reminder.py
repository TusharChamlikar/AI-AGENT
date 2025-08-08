import os
from datetime import date
from dotenv import load_dotenv
from backend.utils.send_reminder import send_reminder
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import requests
from urllib.parse import quote  # Import the quote function
# Load environment variables
load_dotenv()

# Mock Reminder class
class Reminder:
    def __init__(self, name, amount, due_date, contact,email,mobile):
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

import os
from twilio.rest import Client
from urllib.parse import quote  # Import the quote function

def make_twilio_voice_call(reminder):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    to_number = reminder.contact  # must start with '+'

    if account_sid and auth_token and from_number and to_number and to_number.startswith('+'):
        try:
            client = Client(account_sid, auth_token)

            # 1. Create the message content string
            message_content = (
                f"Hello {reminder.name}, this is a payment reminder. "
                f"You have ₹{reminder.amount} due on {reminder.due_date}. Please pay on time."
            )
            
            # 2. URL-encode the message content
            encoded_message = quote(message_content)

            # 3. Construct the TwiML URL with the encoded message
            twiml_url = f"http://twimlets.com/message?Message={encoded_message}"
            
            call = client.calls.create(
                url=twiml_url,
                to=to_number,
                from_=from_number
            )
            print(f"📞 Twilio voice call placed to {to_number} — Call SID: {call.sid}")
        except Exception as e:
            print(f"❌ Twilio Voice error: {e}")
    else:
        print("⚠️ Twilio Voice skipped: missing config or invalid phone number")