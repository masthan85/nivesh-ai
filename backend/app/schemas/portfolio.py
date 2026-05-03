from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HoldingCreate(BaseModel):
    symbol: str
    name: str
    qty: float
    avg_price: float
    sector: str = "Unknown"
    exchange: str = "NSE"
    asset_type: str = "Equity"
    buy_date: str = ""
    notes: str = ""


class HoldingUpdate(BaseModel):
    qty: Optional[float] = None
    avg_price: Optional[float] = None
    sector: Optional[str] = None
    notes: Optional[str] = None


class HoldingOut(BaseModel):
    id: int
    symbol: str
    name: str
    qty: float
    avg_price: float
    sector: str
    exchange: str
    asset_type: str
    buy_date: str
    ltp: float = 0
    change_pct: float = 0
    pnl: float = 0
    pnl_pct: float = 0
    current_value: float = 0
    invested_value: float = 0

    class Config:
        from_attributes = True


class GoalCreate(BaseModel):
    name: str
    icon: str = "🎯"
    target: float
    saved: float = 0
    monthly: float
    years: int
    risk: str = "Moderate"
    color: str = "#4d9fff"


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target: Optional[float] = None
    saved: Optional[float] = None
    monthly: Optional[float] = None
    years: Optional[int] = None
    risk: Optional[str] = None


class WatchCreate(BaseModel):
    symbol: str
    target: Optional[float] = None
    stop_loss: Optional[float] = None
    notes: str = ""


class AlertCreate(BaseModel):
    symbol: str
    alert_type: str   # above | below | crosses
    price: float
    notify_push: bool = True
    notify_email: bool = True


class BrokerCalcRequest(BaseModel):
    price: float
    qty: int
    trade_type: str   # delivery | intraday | fo


class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
