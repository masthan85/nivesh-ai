from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

RiskProfile = Literal['Conservative', 'Moderate', 'Aggressive']

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    risk: RiskProfile = 'Moderate'
    horizon: int = Field(default=7, ge=1, le=60)
    monthly_sip: Decimal = Field(default=Decimal('10000'), ge=0, le=100_000_000, max_digits=24, decimal_places=2)

    @field_validator('password')
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(c.isalpha() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one letter and one number')
        return value

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    risk: str
    horizon: int
    monthly_sip: Decimal
    created_at: datetime
    model_config = {'from_attributes': True}

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    risk: Optional[RiskProfile] = None
    horizon: Optional[int] = Field(default=None, ge=1, le=60)
    monthly_sip: Optional[Decimal] = Field(default=None, ge=0, le=100_000_000, max_digits=24, decimal_places=2)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
