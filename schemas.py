from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LogoutRequest(BaseModel):
    token: str

class CarRequest(BaseModel):
    plate_number: str
    brand: str
    model: str
    year: int

class CarResponse(BaseModel):
    id: int
    plate_number: str
    brand: str
    model: str
    year: int
    rejection_report: Optional[str]
    rejection_count: int
    approved_count: int

    class Config:
        from_attributes = True

class RejectCarRequest(BaseModel):
    rejection_report: str