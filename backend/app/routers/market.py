from fastapi import APIRouter, Query
from app.services.market_data import get_quote, get_full_quote, search_symbol

router = APIRouter(prefix='/market', tags=['Market Data'])


@router.get('/price/{symbol}')
def price(symbol: str):
    return get_quote(symbol.upper()).to_dict()


@router.get('/prices')
def bulk_prices(symbols: str = Query(min_length=1, max_length=500)):
    result = {}
    for sym in symbols.split(',')[:50]:
        clean = sym.strip().upper()
        if clean:
            result[clean] = get_quote(clean).to_dict()
    return result


@router.get('/quote/{symbol}')
def full_quote(symbol: str):
    return get_full_quote(symbol.upper())


@router.get('/search/{query}')
def search(query: str):
    return search_symbol(query)
