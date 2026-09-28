from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from decimal import Decimal
from typing import Protocol, Optional


@dataclass(frozen=True)
class Quote:
    symbol: str
    price: Optional[Decimal]
    previous_close: Optional[Decimal]
    as_of: datetime
    source: str
    freshness: str
    is_live: bool
    error: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data['price'] = float(self.price) if self.price is not None else None
        data['previous_close'] = float(self.previous_close) if self.previous_close is not None else None
        data['as_of'] = self.as_of.isoformat()
        return data


class MarketDataProvider(Protocol):
    name: str

    def get_quote(self, symbol: str) -> Quote:
        ...


class UnavailableMarketDataProvider:
    name = 'unavailable'

    def get_quote(self, symbol: str) -> Quote:
        return Quote(
            symbol=symbol.upper(),
            price=None,
            previous_close=None,
            as_of=datetime.now(timezone.utc),
            source=self.name,
            freshness='unavailable',
            is_live=False,
            error='No production market-data provider is configured.',
        )
