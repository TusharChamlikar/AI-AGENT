import os
import base64
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from twilio.rest import Client
from urllib.parse import quote
from openai import OpenAI
from datetime import datetime

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
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that writes concise, friendly SMS reminders."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ OpenAI SMS generation failed: {e}")
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
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Payment Reminder</title>
                <style>
                    body {{ margin: 0; padding: 0; background-color: #f4f6f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; }}
                    .header {{ background-color: #4f46e5; color: #ffffff; padding: 24px; text-align: center; }}
                    .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
                    .content {{ padding: 32px; color: #333; line-height: 1.6; }}
                    .content-info {{ background-color: #f1f5f9; border-radius: 8px; padding: 20px; text-align: center; margin: 16px 0; }}
                    .content-info .amount {{ font-size: 36px; font-weight: 700; color: #1e293b; margin: 0 0 8px 0; }}
                    .content-info .due-date {{ font-size: 16px; color: #475569; margin: 0; }}
                    .cta-button {{ display: block; width: fit-content; margin: 24px auto 0 auto; padding: 14px 28px; background-color: #4f46e5; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 500; }}
                    .footer {{ padding: 24px; text-align: center; font-size: 12px; color: #64748b; }}
                </style>
            </head>
            <body>
                <table width="100%" border="0" cellspacing="0" cellpadding="20" style="background-color: #f4f6f8;">
                    <tr>
                        <td align="center">
                            <table class="container" border="0" cellspacing="0" cellpadding="0" style="width: 100%; max-width: 600px;">
                                <tr><td class="header"><h1>Fin-Minder</h1></td></tr>
                                <tr>
                                    <td class="content">
                                        <p>Hi {reminder.name},</p>
                                        <p>This is a friendly reminder for your upcoming payment.</p>
                                        <div class="content-info">
                                            <p class="amount">₹{reminder.amount}</p>
                                            <p class="due-date">Due on: {reminder.due_date}</p>
                                        </div>
                                        <p>Please ensure the payment is made on or before the due date to avoid any late fees. If you've already made the payment, please disregard this email.</p>
                                        <a href="#" class="cta-button" style="color: #ffffff !important;">Pay Now</a>

                                    </td>
                                </tr>
                                <tr><td class="footer"><p>&copy; {datetime.now().year} Fin-Minder. All rights reserved.</p></td></tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=f"Reminder: Payment of ₹{reminder.amount} due",
                html_content=html_content
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
            sms_body = generate_smart_sms(reminder)
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
                "voice_settings": { "stability": 0.5, "similarity_boost": 0.75 }
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
                        html_content=f"<p>Hi {reminder.name}, attached is a voice reminder for your upcoming payment.</p>"
                    )
                    voice_email.attachment = attachment
                    sg = SendGridAPIClient(sg_api_key)
                    sg.send(voice_email)
                    print("🎧 Voice email with MP3 sent successfully")
                else:
                    print("⚠️ Voice email skipped: invalid SendGrid config")
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
        to_number = reminder.mobile

        if account_sid and auth_token and from_number and to_number and to_number.startswith('+'):
            client = Client(account_sid, auth_token)
            message_content = (f"Hello {reminder.name}, this is a payment reminder. "
                             f"You have ₹{reminder.amount} due on {reminder.due_date}. Please pay on time.")
            encoded_message = quote(message_content)
            twiml_url = f"https://twimlets.com/message?Message={encoded_message}"
            
            call = client.calls.create(url=twiml_url, to=to_number, from_=from_number)
            print(f"📞 Twilio voice call placed to {to_number} — Call SID: {call.sid}")
        else:
            print("⚠️ Twilio Voice skipped: missing config or invalid phone number")
    except Exception as e:
        print(f"❌ Twilio Voice error: {e}")