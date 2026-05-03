from datetime import datetime
from typing import Dict, Tuple, Optional

# In-memory cache: symbol -> (price, change_pct, cached_at)
_cache: Dict[str, Tuple[float, float, datetime]] = {}
CACHE_TTL_SECONDS = 60


def get_cached_price(symbol: str) -> Optional[Tuple[float, float]]:
    if symbol in _cache:
        price, chg, ts = _cache[symbol]
        if (datetime.utcnow() - ts).total_seconds() < CACHE_TTL_SECONDS:
            return price, chg
    return None


def set_cached_price(symbol: str, price: float, change_pct: float):
    _cache[symbol] = (price, change_pct, datetime.utcnow())


def clear_cache():
    _cache.clear()
