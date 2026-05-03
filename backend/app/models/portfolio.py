from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Holding(Base):
    __tablename__ = "holdings"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol      = Column(String(20), nullable=False)
    name        = Column(String(200), nullable=False)
    qty         = Column(Float, nullable=False)
    avg_price   = Column(Float, nullable=False)
    sector      = Column(String(50), default="Unknown")
    exchange    = Column(String(10), default="NSE")
    asset_type  = Column(String(20), default="Equity")  # Equity | MF | ETF | Unlisted | Bond
    buy_date    = Column(String(20), default="")
    notes       = Column(Text, default="")
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="holdings")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    role       = Column(String(10), nullable=False)   # user | assistant
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_messages")
