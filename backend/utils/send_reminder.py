import os
import base64
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from twilio.rest import Client
from urllib.parse import quote  # Import the quote function
load_dotenv()

def send_reminder(reminder):
    """
    Sends a reminder via Email (SendGrid), SMS (Twilio), and Voice (ElevenLabs with MP3 email attachment).
    """
    print(f"🔔 Reminder: {reminder.name}, ₹{reminder.amount} due on {reminder.due_date}")

    # === Email Reminder ===
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

    # === SMS Reminder ===
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

    # === Voice Reminder via ElevenLabs ===
    try:
        eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
        voice_id = os.getenv("ELEVENLABS_VOICE_ID")

        if eleven_api_key and voice_id:
            text = f"Hi {reminder.name}, this is a reminder. You have a payment of ₹{reminder.amount} due on {reminder.due_date}. Please pay it on time."
            headers = {
                "xi-api-key": eleven_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                file_path = f"{reminder.name}_reminder.mp3"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print("🔊 Voice reminder generated with ElevenLabs")

                # Send email with voice MP3 attachment
                if sg_api_key and from_email and to_email and "@" in to_email:
                    with open(file_path, "rb") as audio_file:
                        encoded_file = base64.b64encode(audio_file.read()).decode()

                    attachment = Attachment(
                        FileContent(encoded_file),
                        FileName(f"{reminder.name}_reminder.mp3"),
                        FileType("audio/mpeg"),
                        Disposition("attachment")
                    )

                    voice_email = Mail(
                        from_email=from_email,
                        to_emails=to_email,
                        subject=f"Voice Reminder: ₹{reminder.amount} due",
                        html_content=f"""
                            <p>Hi {reminder.name},</p>
                            <p>Attached is a voice reminder for your upcoming payment of ₹{reminder.amount} due on <strong>{reminder.due_date}</strong>.</p>
                            <p>— PayMind AI</p>
                        """
                    )
                    voice_email.attachment = attachment
                    sg = SendGridAPIClient(sg_api_key)
                    sg.send(voice_email)
                    print("🎧 Voice email with MP3 sent successfully")
                else:
                    print("⚠️ Voice email skipped: invalid SendGrid config or contact email")
            else:
                print(f"⚠️ ElevenLabs voice failed: {response.status_code} - {response.text}")
        else:
            print("🟡 Voice not triggered: ELEVENLABS_API_KEY or VOICE_ID not set")
    except Exception as e:
        print(f"❌ ElevenLabs voice error: {e}")

# === Twilio Voice Call ===
    try: 
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        to_number = reminder.contact  # must start with '+'

        if account_sid and auth_token and from_number and to_number and to_number.startswith('+'):
            client = Client(account_sid, auth_token)
    
            # The message content to be URL-encoded
            message_content = (
                f"Hello {reminder.name}, this is a payment reminder. "
                f"You have ₹{reminder.amount} due on {reminder.due_date}. Please pay on time."
            )

            # URL-encode the message content
            encoded_message = quote(message_content)

            # Construct the final TwiML URL with the encoded message
            twiml_url = f"https://twimlets.com/message?Message={encoded_message}"
            
            print(f"DEBUG: TwiML URL being used: {twiml_url}")
            call = client.calls.create(
                            url=twiml_url,
                            to=to_number,
                            from_=from_number
            )
            print(f"📞 Twilio voice call placed to {to_number} — Call SID: {call.sid}")
        else:
            print("⚠️ Twilio Voice skipped: missing config or invalid phone number")
    except Exception as e:
        print(f"❌ Twilio Voice error: {e}")
