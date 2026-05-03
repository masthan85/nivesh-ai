"""routers/market.py"""
from fastapi import APIRouter
from app.services.market_data import get_live_price, get_full_quote, search_symbol

router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/price/{symbol}")
def live_price(symbol: str):
    ltp, chg = get_live_price(symbol.upper())
    return {"symbol": symbol.upper(), "ltp": ltp, "change_pct": chg}


@router.get("/prices")
def bulk_prices(symbols: str):
    result = {}
    for sym in symbols.split(","):
        sym = sym.strip().upper()
        ltp, chg = get_live_price(sym)
        result[sym] = {"ltp": ltp, "change_pct": chg}
    return result


@router.get("/quote/{symbol}")
def full_quote(symbol: str):
    return get_full_quote(symbol.upper())


@router.get("/search/{query}")
def search(query: str):
    return search_symbol(query)
