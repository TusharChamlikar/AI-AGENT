from sqlalchemy import Column, Integer, String, Boolean, Date
from backend.db import Base


class Reminder(Base):
    __tablename__ = "reminder"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    email = Column(String(100), nullable=True)
    mobile = Column(String(100),nullable=True)
    notified = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "due_date": self.due_date.isoformat(),  # Convert date to string
            "email": self.email,
            "mobile":self.email,
            "notified": self.notified
        }