from __future__ import annotations
from decimal import Decimal
from functools import lru_cache
from typing import Dict, Any
from app.config import settings
from app.domain.money import percent
from app.providers.market_data import MarketDataProvider, Quote, UnavailableMarketDataProvider


@lru_cache
def get_provider() -> MarketDataProvider:
    if settings.MARKET_DATA_MODE.lower() in {'development', 'yfinance'}:
        from app.providers.yfinance_provider import YFinanceDevelopmentProvider
        return YFinanceDevelopmentProvider()
    return UnavailableMarketDataProvider()


def get_quote(symbol: str) -> Quote:
    return get_provider().get_quote(symbol)


def get_live_price(symbol: str):
    """Legacy compatibility wrapper. Prefer get_quote so freshness/source metadata is retained."""
    quote = get_quote(symbol)
    if quote.price is None:
        return 0.0, 0.0
    prev = quote.previous_close or quote.price
    change = Decimal('0') if not prev else (quote.price - prev) / prev * Decimal('100')
    return float(quote.price), float(percent(change))


def get_full_quote(symbol: str) -> Dict[str, Any]:
    quote = get_quote(symbol)
    data = quote.to_dict()
    if quote.price is None:
        return data
    prev = quote.previous_close or quote.price
    change = quote.price - prev
    change_pct = Decimal('0') if not prev else change / prev * Decimal('100')
    data.update({
        'ltp': float(quote.price),
        'prev_close': float(prev),
        'change': float(change.quantize(Decimal('0.01'))),
        'change_pct': float(percent(change_pct)),
    })
    return data


def search_symbol(query: str) -> list:
    # Symbol search is intentionally disabled until a provider with explicit search/licensing is configured.
    return []
