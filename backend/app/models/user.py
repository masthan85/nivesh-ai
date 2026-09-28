from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(100), nullable=False)
    email        = Column(String(255), unique=True, index=True, nullable=False)
    hashed_pw    = Column(String(255), nullable=False)
    risk         = Column(String(20), default="Moderate")   # Conservative | Moderate | Aggressive
    horizon      = Column(Integer, default=7)               # investment horizon in years
    monthly_sip  = Column(Numeric(24, 2), default=0)
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    holdings     = relationship("Holding",    back_populates="user", cascade="all, delete-orphan")
    goals        = relationship("Goal",       back_populates="user", cascade="all, delete-orphan")
    watchlist    = relationship("WatchItem",  back_populates="user", cascade="all, delete-orphan")
    alerts       = relationship("PriceAlert", back_populates="user", cascade="all, delete-orphan")
    chat_messages= relationship("ChatMessage",back_populates="user", cascade="all, delete-orphan")
