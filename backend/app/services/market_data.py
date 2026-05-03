from typing import Tuple, Dict, Any
import yfinance as yf
from app.utils.cache import get_cached_price, set_cached_price


def get_live_price(symbol: str) -> Tuple[float, float]:
    """Fetch live price for a symbol. Returns (price, change_pct)."""
    cached = get_cached_price(symbol)
    if cached:
        return cached

    for suffix in [".NS", ".BO", ""]:
        try:
            ticker = yf.Ticker(symbol + suffix)
            info = ticker.fast_info
            price = float(getattr(info, "last_price", 0) or 0)
            prev  = float(getattr(info, "previous_close", price) or price)
            if price > 0:
                chg = round((price - prev) / prev * 100, 2) if prev else 0
                set_cached_price(symbol, round(price, 2), chg)
                return round(price, 2), chg
        except Exception:
            continue

    return 0.0, 0.0


def get_full_quote(symbol: str) -> Dict[str, Any]:
    """Full quote with fundamentals and 30-day history."""
    try:
        ticker = yf.Ticker(symbol + ".NS")
        info = ticker.info
        hist = ticker.history(period="1mo")
        current = info.get("currentPrice") or info.get("regularMarketPrice", 0)
        prev    = info.get("previousClose", current)
        return {
            "symbol":        symbol.upper(),
            "name":          info.get("longName", symbol),
            "ltp":           round(current, 2),
            "prev_close":    round(prev, 2),
            "change":        round(current - prev, 2),
            "change_pct":    round((current - prev) / prev * 100, 2) if prev else 0,
            "open":          info.get("open", 0),
            "high":          info.get("dayHigh", 0),
            "low":           info.get("dayLow", 0),
            "volume":        info.get("volume", 0),
            "market_cap":    info.get("marketCap", 0),
            "pe":            info.get("trailingPE", 0),
            "pb":            info.get("priceToBook", 0),
            "eps":           info.get("trailingEps", 0),
            "week52_high":   info.get("fiftyTwoWeekHigh", 0),
            "week52_low":    info.get("fiftyTwoWeekLow", 0),
            "dividend_yield":info.get("dividendYield", 0),
            "sector":        info.get("sector", "Unknown"),
            "industry":      info.get("industry", "Unknown"),
            "history":       hist["Close"].round(2).tolist() if not hist.empty else [],
            "history_dates": [d.strftime("%Y-%m-%d") for d in hist.index] if not hist.empty else [],
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e), "ltp": 0}


def search_symbol(query: str) -> list:
    """Search for a stock symbol."""
    results = []
    for suffix in [".NS", ".BO"]:
        try:
            t = yf.Ticker(query.upper() + suffix)
            info = t.info
            name = info.get("longName") or info.get("shortName", "")
            if name:
                results.append({
                    "symbol":   query.upper(),
                    "name":     name,
                    "exchange": "NSE" if suffix == ".NS" else "BSE",
                    "sector":   info.get("sector", "Unknown"),
                    "ltp":      info.get("currentPrice", 0),
                })
                break
        except Exception:
            continue
    return results
