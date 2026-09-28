from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Holding(Base):
    __tablename__ = "holdings"
    __table_args__ = (UniqueConstraint("user_id", "symbol", "exchange", name="uq_holding_user_symbol_exchange"),)

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol      = Column(String(20), nullable=False)
    name        = Column(String(200), nullable=False)
    qty         = Column(Numeric(24, 8), nullable=False)
    avg_price   = Column(Numeric(24, 4), nullable=False)
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
