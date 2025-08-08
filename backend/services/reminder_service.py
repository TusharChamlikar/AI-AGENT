from backend.models.reminder_model import Reminder
from backend.db import SessionLocal
from datetime import date

def create_reminder(name, amount, due_date, email,mobile):
    db = SessionLocal()
    reminder = Reminder(
        name=name,
        amount=amount,
        due_date=due_date,
        email=email,
        mobile=mobile
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    db.close()
    return reminder

def get_due_reminders():
    db = SessionLocal()
    reminders = db.query(Reminder).filter(
        Reminder.due_date <= date.today(),
        Reminder.notified == False
    ).all()
    db.close()
    return reminders
