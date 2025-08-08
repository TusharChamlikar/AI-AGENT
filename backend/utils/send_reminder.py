import os
import base64
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from twilio.rest import Client
from urllib.parse import quote
from openai import OpenAI  # ✅ Added for AI-generated SMS

load_dotenv()

# Initialize OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_smart_sms(reminder):
    """Use OpenAI to generate a short, friendly SMS."""
    prompt = f"""
    Write a concise, friendly payment reminder for {reminder.name}.
    Amount due: ₹{reminder.amount}
    Due date: {reminder.due_date}
    Keep it under 160 characters, polite, and clear.
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight, fast
            messages=[
                {"role": "system", "content": "You are an assistant that writes concise, friendly SMS reminders."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ OpenAI SMS generation failed: {e}")
        # Fallback: normal static message
        return f"Reminder: ₹{reminder.amount} is due on {reminder.due_date}, {reminder.name}."

def send_reminder(reminder):
    """
    Sends a reminder via Email (SendGrid), SMS (Twilio with OpenAI),
    and Voice (ElevenLabs with MP3 email attachment), plus Twilio voice call.
    """
    print(f"🔔 Reminder: {reminder.name}, ₹{reminder.amount} due on {reminder.due_date}")

    # === Email Reminder ===
    try:
        sg_api_key = os.getenv("SENDGRID_API_KEY")
        from_email = os.getenv("FROM_EMAIL")
        to_email = reminder.email

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

    # === SMS Reminder with OpenAI ===
    try:
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        to_number = reminder.mobile

        if twilio_sid and twilio_token and from_number and to_number and to_number.startswith("+"):
            client = Client(twilio_sid, twilio_token)
            sms_body = generate_smart_sms(reminder)  # ✅ AI-generated
            message = client.messages.create(
                body=sms_body,
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
        to_number = reminder.mobile  # must start with '+'

        if account_sid and auth_token and from_number and to_number and to_number.startswith('+'):
            client = Client(account_sid, auth_token)
    
            message_content = (
                f"Hello {reminder.name}, this is a payment reminder. "
                f"You have ₹{reminder.amount} due on {reminder.due_date}. Please pay on time."
            )

            encoded_message = quote(message_content)
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
