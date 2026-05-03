from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    risk: str = "Moderate"
    horizon: int = 7
    monthly_sip: float = 10000


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    risk: str
    horizon: int
    monthly_sip: float
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    risk: Optional[str] = None
    horizon: Optional[int] = None
    monthly_sip: Optional[float] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
