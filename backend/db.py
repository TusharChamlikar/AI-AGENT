# backend/db.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/paymind_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connected successfully.")
    except OperationalError as e:
        print("❌ Database connection failed.")
        print(str(e))

if __name__ == "__main__":
    test_connection()
