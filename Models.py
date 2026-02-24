from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from typing import Optional

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

    status = Column(String, default="pending")  # pending / approved / rejected
    rejection_report = Column(String, nullable=True)
    rejection_count = Column(Integer, default=0)
    approved_count = Column(Integer, default=0)