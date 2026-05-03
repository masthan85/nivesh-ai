from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    name       = Column(String(100), nullable=False)
    icon       = Column(String(10), default="🎯")
    target     = Column(Float, nullable=False)
    saved      = Column(Float, default=0)
    monthly    = Column(Float, nullable=False)
    years      = Column(Integer, nullable=False)
    risk       = Column(String(20), default="Moderate")
    color      = Column(String(10), default="#4d9fff")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="goals")


class WatchItem(Base):
    __tablename__ = "watchlist"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol     = Column(String(20), nullable=False)
    target     = Column(Float, nullable=True)
    stop_loss  = Column(Float, nullable=True)
    notes      = Column(String(500), default="")
    added_at   = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="watchlist")


class PriceAlert(Base):
    __tablename__ = "alerts"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol       = Column(String(20), nullable=False)
    alert_type   = Column(String(10), nullable=False)   # above | below | crosses
    price        = Column(Float, nullable=False)
    notify_push  = Column(Boolean, default=True)
    notify_email = Column(Boolean, default=True)
    status       = Column(String(10), default="active")  # active | triggered | disabled
    created_at   = Column(DateTime, default=datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="alerts")
