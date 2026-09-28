from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
import yfinance as yf
from app.providers.market_data import Quote


class YFinanceDevelopmentProvider:
    """Development-only adapter. Yahoo Finance data is not treated as a licensed production feed."""

    name = 'yfinance-development'

    def get_quote(self, symbol: str) -> Quote:
        for suffix in ['.NS', '.BO', '']:
            try:
                ticker = yf.Ticker(symbol + suffix)
                info = ticker.fast_info
                raw_price = getattr(info, 'last_price', None)
                if raw_price is None or float(raw_price) <= 0:
                    continue
                raw_prev = getattr(info, 'previous_close', raw_price) or raw_price
                return Quote(
                    symbol=symbol.upper(),
                    price=Decimal(str(raw_price)),
                    previous_close=Decimal(str(raw_prev)),
                    as_of=datetime.now(timezone.utc),
                    source=self.name,
                    freshness='best-effort/development',
                    is_live=False,
                )
            except Exception:
                continue
        return Quote(
            symbol=symbol.upper(),
            price=None,
            previous_close=None,
            as_of=datetime.now(timezone.utc),
            source=self.name,
            freshness='unavailable',
            is_live=False,
            error='Quote unavailable from development provider.',
        )
