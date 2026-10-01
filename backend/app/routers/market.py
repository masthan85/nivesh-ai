"""Market data routes. Authenticated so the application is not an open proxy to its data provider."""
from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.models.user import User
from app.services.market_data import get_full_quote, get_quote, search_symbol
from app.utils.auth import get_current_user

router = APIRouter(prefix='/market', tags=['Market Data'], dependencies=[Depends(get_current_user)])

SYMBOL_PATTERN = r'^[A-Za-z0-9._&-]{1,20}$'
MAX_BULK_SYMBOLS = 50


@router.get('/price/{symbol}')
def price(symbol: str = Path(pattern=SYMBOL_PATTERN)):
    return get_quote(symbol.upper()).to_dict()


@router.get('/prices')
def bulk_prices(symbols: str = Query(min_length=1, max_length=1100)):
    cleaned = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    if len(cleaned) > MAX_BULK_SYMBOLS:
        raise HTTPException(status_code=422, detail=f'At most {MAX_BULK_SYMBOLS} symbols per request')
    return {s: get_quote(s).to_dict() for s in cleaned}


@router.get('/quote/{symbol}')
def full_quote(symbol: str = Path(pattern=SYMBOL_PATTERN)):
    return get_full_quote(symbol.upper())


@router.get('/search/{query}')
def search(query: str = Path(min_length=1, max_length=50)):
    return {'status': 'unavailable', 'reason': 'Instrument search needs a licensed provider.', 'results': search_symbol(query)}
