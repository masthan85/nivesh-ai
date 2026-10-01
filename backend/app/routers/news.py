"""News for the user's holdings.

Development-only: headlines come from the yfinance adapter, which is not a licensed news
source. Sentiment and impact are not assessed, so they are not reported.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.portfolio import Holding
from app.models.user import User
from app.utils.auth import get_current_user

news_router = APIRouter(prefix="/news", tags=["News"])

SOURCE = "yfinance-development"


def _news_enabled() -> bool:
    return settings.MARKET_DATA_MODE.lower() in {"development", "yfinance"}


def _item(symbol, item: dict) -> dict:
    # yfinance has returned both flat and nested ("content") shapes across versions.
    content = item.get("content") if isinstance(item.get("content"), dict) else item
    link = content.get("link") or (content.get("canonicalUrl") or {}).get("url") or ""
    publisher = content.get("publisher") or (content.get("provider") or {}).get("displayName") or ""
    return {
        "symbol": symbol,
        "title": content.get("title", ""),
        "publisher": publisher,
        "link": link,
        "published": content.get("providerPublishTime") or content.get("pubDate") or "",
        "source": SOURCE,
    }


def _fetch(ticker_symbol: str, limit: int) -> list:
    import yfinance as yf
    try:
        return (yf.Ticker(ticker_symbol).news or [])[:limit]
    except Exception:
        return []


@news_router.get("/portfolio")
def portfolio_news(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not _news_enabled():
        return {"status": "unavailable", "reason": "No news provider is configured.", "items": []}
    holdings = db.query(Holding).filter(Holding.user_id == user.id).limit(6).all()
    items = [_item(h.symbol, raw) for h in holdings for raw in _fetch(h.symbol + ".NS", 2)]
    return {"status": "development-source", "items": [i for i in items if i["title"]]}


@news_router.get("/market")
def market_news(user: User = Depends(get_current_user)):
    if not _news_enabled():
        return {"status": "unavailable", "reason": "No news provider is configured.", "items": []}
    items = [_item(None, raw) for raw in _fetch("^NSEI", 10)]
    return {"status": "development-source", "items": [i for i in items if i["title"]]}
