from backend.db import Base, engine
from backend.models.reminder_model import Reminder

Base.metadata.create_all(bind=engine)

print("✅ Tables created.")
