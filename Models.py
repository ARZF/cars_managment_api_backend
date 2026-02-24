from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)

    rejection_report = Column(String, nullable=True)
    rejection_count = Column(Integer, default=0)
    approved_count = Column(Integer, default=0)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    reason = Column(String)
    car_id = Column(Integer, ForeignKey("cars.id"))
    user_id = Column(Integer, ForeignKey("users.id"))