# create a databse to save the booking info and meta data 

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime 
import os 




base = declarative_base()

class Document(base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String(100), unique=True)
    filename = Column(String(255))
    upload_time = Column(DateTime, default=datetime.utcnow)

class Booking(base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    date = Column(String(50))
    time = Column(String(50))
    booking_time = Column(DateTime, default=datetime.utcnow) 


DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=False)
base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

class DatabaseService:
    def save_document_metadata(self, document_id: str, filename: str):
        db = SessionLocal()
        try:
            doc = Document(document_id=document_id, filename=filename)
            db.add(doc)
            db.commit()
        finally:
            db.close()

    def save_booking(self, name: str, email: str, date: str, time: str):
        db = SessionLocal()
        try:
            booking = Booking(name=name, email=email, date=date, time=time)
            db.add(booking)
            db.commit()
            return {"status": "success", "message": "Booking saved in MySQL"}
        finally:
            db.close()

db_service = DatabaseService()