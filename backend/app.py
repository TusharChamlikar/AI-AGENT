from fastapi import FastAPI
from routes.reminder_routes import router as reminder_router

app = FastAPI()
app.include_router(reminder_router)

@app.get("/")
def home():
    return {"message": "AI Payment Reminder Agent is Live"}
