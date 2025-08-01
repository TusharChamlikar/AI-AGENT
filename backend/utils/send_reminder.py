import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

def send_reminder(reminder):
    """
    Sends a reminder via Email (SendGrid), SMS (Twilio), and optionally Voice via n8n webhook.
    """
    # Print to console for visibility
    print(f"🔔 Reminder: {reminder.name}, ₹{reminder.amount} due on {reminder.due_date}")

    # === Email Reminder via SendGrid ===
    try:
        sg_api_key = os.getenv("SENDGRID_API_KEY")
        from_email = os.getenv("FROM_EMAIL")
        to_email = reminder.contact

        if sg_api_key and from_email and to_email and "@" in to_email:
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=f"Reminder: Payment of ₹{reminder.amount} due",
                html_content=f"""
                    <p>Hi {reminder.name},</p>
                    <p>This is a friendly reminder that you have a payment of ₹{reminder.amount} due on <strong>{reminder.due_date}</strong>.</p>
                    <p>Please make sure to complete it in time. Thank you!</p>
                    <p>— PayMind AI Reminder Agent</p>
                """
            )
            sg = SendGridAPIClient(sg_api_key)
            sg.send(message)
            print(f"📧 Email sent to {to_email}")
        else:
            print("⚠️ Email skipped: invalid or missing configuration/contact")

    except Exception as e:
        print(f"❌ Email error: {e}")

    # === SMS Reminder via Twilio ===
    try:
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        to_number = reminder.contact

        if twilio_sid and twilio_token and from_number and to_number and to_number.startswith("+"):
            client = Client(twilio_sid, twilio_token)
            message = client.messages.create(
                body=f"Reminder: ₹{reminder.amount} is due on {reminder.due_date}, {reminder.name}.",
                from_=from_number,
                to=to_number
            )
            print(f"📱 SMS sent to {to_number}, SID: {message.sid}")
        else:
            print("⚠️ SMS skipped: invalid or missing configuration/contact")

    except Exception as e:
        print(f"❌ SMS error: {e}")

    # === Optional: Trigger n8n Voice Flow (Retell/ElevenLabs) ===
    try:
        if os.getenv("N8N_WEBHOOK_URL"):
            webhook_url = os.getenv("N8N_WEBHOOK_URL")
            response = requests.post(webhook_url, json={
                "name": reminder.name,
                "amount": reminder.amount,
                "due_date": str(reminder.due_date),
                "contact": reminder.contact
            })
            print(f"📞 Voice reminder triggered via n8n. Status: {response.status_code}")
        else:
            print("🟡 Voice not triggered: N8N_WEBHOOK_URL not set")
    except Exception as e:
        print(f"❌ Voice webhook error: {e}")
