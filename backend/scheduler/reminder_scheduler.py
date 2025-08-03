from apscheduler.schedulers.background import BackgroundScheduler
from backend.services.reminder_service import get_due_reminders

from backend.utils.send_reminder import send_reminder


scheduler = BackgroundScheduler()

def check_due_reminders():
    print("🔍 Checking for due reminders...")
    reminders = get_due_reminders()
    for reminder in reminders:
        print(f"📣 Sending reminder to {reminder.name}, Amount: ₹{reminder.amount}")
        send_reminder(reminder)  # SMS, email, voice logic
        reminder.notified = True

        from backend.db import SessionLocal
        db = SessionLocal()
        db.merge(reminder)
        db.commit()
        db.close()

def start_scheduler():
    scheduler.add_job(check_due_reminders, 'interval', minutes=1)  # use hours=1 in prod
    scheduler.start()

