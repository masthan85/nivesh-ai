from decimal import Decimal
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, field_validator

Money = Decimal

# Constraints live inside Annotated so they also apply when the field is Optional.
# (pydantic 2.7 rejects max_digits/decimal_places on Optional[Decimal] via Field.)
Quantity = Annotated[Decimal, Field(gt=0, max_digits=24, decimal_places=8)]
Price = Annotated[Decimal, Field(gt=0, max_digits=24, decimal_places=4)]
PositiveMoney = Annotated[Decimal, Field(gt=0, max_digits=24, decimal_places=2)]
NonNegativeMoney = Annotated[Decimal, Field(ge=0, max_digits=24, decimal_places=2)]

class HoldingCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20, pattern=r'^[A-Za-z0-9._-]+$')
    name: str = Field(min_length=1, max_length=200)
    qty: Decimal = Field(gt=0, max_digits=24, decimal_places=8)
    avg_price: Decimal = Field(gt=0, max_digits=24, decimal_places=4)
    sector: str = Field(default='Unknown', max_length=50)
    exchange: str = Field(default='NSE', max_length=10)
    asset_type: str = Field(default='Equity', max_length=20)
    buy_date: str = Field(default='', max_length=20)
    notes: str = Field(default='', max_length=2000)

    @field_validator('symbol')
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper().strip()

class HoldingUpdate(BaseModel):
    qty: Optional[Quantity] = None
    avg_price: Optional[Price] = None
    sector: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = Field(default=None, max_length=2000)

class GoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    icon: str = 'Goal'
    target: Decimal = Field(gt=0, max_digits=24, decimal_places=2)
    saved: Decimal = Field(default=Decimal('0'), ge=0, max_digits=24, decimal_places=2)
    monthly: Decimal = Field(ge=0, max_digits=24, decimal_places=2)
    years: int = Field(ge=1, le=60)
    risk: Literal['Conservative', 'Moderate', 'Aggressive'] = 'Moderate'
    color: str = '#4d9fff'

class GoalUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    target: Optional[PositiveMoney] = None
    saved: Optional[NonNegativeMoney] = None
    monthly: Optional[NonNegativeMoney] = None
    years: Optional[int] = Field(default=None, ge=1, le=60)
    risk: Optional[Literal['Conservative', 'Moderate', 'Aggressive']] = None

class WatchCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20, pattern=r'^[A-Za-z0-9._-]+$')
    target: Optional[Price] = None
    stop_loss: Optional[Price] = None
    notes: str = Field(default='', max_length=500)

class AlertCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20, pattern=r'^[A-Za-z0-9._-]+$')
    alert_type: Literal['above', 'below', 'crosses']
    price: Decimal = Field(gt=0, max_digits=24, decimal_places=4)
    notify_push: bool = True
    notify_email: bool = True

TradeType = Literal['delivery', 'intraday', 'fo']


class BrokerCalcRequest(BaseModel):
    price: Decimal = Field(gt=0, max_digits=24, decimal_places=4)
    qty: int = Field(gt=0, le=10_000_000)
    trade_type: Literal['delivery', 'intraday', 'fo']

class ChatRequest(BaseModel):
    # Conversation history is loaded from the server's own store, never taken from the client,
    # so a client cannot forge earlier assistant turns or inject system-style instructions.
    model_config = {'extra': 'forbid'}

    message: str = Field(min_length=1, max_length=4000)
