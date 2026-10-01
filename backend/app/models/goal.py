from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.domain.clock import utc_now_naive
from app.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    name       = Column(String(100), nullable=False)
    icon       = Column(String(10), default="🎯")
    target     = Column(Numeric(24, 2), nullable=False)
    saved      = Column(Numeric(24, 2), default=0)
    monthly    = Column(Numeric(24, 2), nullable=False)
    years      = Column(Integer, nullable=False)
    risk       = Column(String(20), default="Moderate")
    color      = Column(String(10), default="#4d9fff")
    created_at = Column(DateTime, default=utc_now_naive)

    user = relationship("User", back_populates="goals")


class WatchItem(Base):
    __tablename__ = "watchlist"
    __table_args__ = (UniqueConstraint("user_id", "symbol", name="uq_watchlist_user_symbol"),)

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol     = Column(String(20), nullable=False)
    target     = Column(Numeric(24, 4), nullable=True)
    stop_loss  = Column(Numeric(24, 4), nullable=True)
    notes      = Column(String(500), default="")
    added_at   = Column(DateTime, default=utc_now_naive)

    user = relationship("User", back_populates="watchlist")


class PriceAlert(Base):
    __tablename__ = "alerts"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol       = Column(String(20), nullable=False)
    alert_type   = Column(String(10), nullable=False)   # above | below | crosses
    price        = Column(Numeric(24, 4), nullable=False)
    notify_push  = Column(Boolean, default=True)
    notify_email = Column(Boolean, default=True)
    status       = Column(String(10), default="active")  # active | triggered | disabled
    created_at   = Column(DateTime, default=utc_now_naive)
    triggered_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="alerts")
