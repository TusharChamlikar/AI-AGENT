from fastapi import APIRouter
from pydantic import BaseModel
from services.openai_agent import generate_payment_reminder  # assuming this is implemented

router = APIRouter()

class ReminderRequest(BaseModel):
    name: str
    amount: float
    due_date: str  # or datetime

@router.post("/reminder")
def trigger_reminder(data: ReminderRequest):
    reminder_text = generate_payment_reminder(data.name, data.amount, data.due_date)
    return {"reminder": reminder_text}
