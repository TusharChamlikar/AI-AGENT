import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_payment_reminder(name: str, amount: float, due_date: str) -> str:
    # Replace with OpenAI call later
    return f"Hi {name}, your payment of ₹{amount} is due on {due_date}. Please pay on time to avoid penalties."
