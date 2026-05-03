"""routers/news.py"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import yfinance as yf
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.utils.auth import get_current_user

news_router = APIRouter(prefix="/news", tags=["News"])


@news_router.get("/portfolio")
def portfolio_news(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    news = []
    for h in holdings[:6]:
        try:
            ticker = yf.Ticker(h.symbol + ".NS")
            for item in (ticker.news or [])[:2]:
                news.append({
                    "symbol":    h.symbol,
                    "title":     item.get("title", ""),
                    "publisher": item.get("publisher", ""),
                    "link":      item.get("link", "#"),
                    "time":      item.get("providerPublishTime", 0),
                    "sentiment": "neutral",
                    "impact":    "MED",
                })
        except Exception:
            continue
    news.sort(key=lambda x: -x["time"])
    return news


@news_router.get("/market")
def market_news():
    try:
        ticker = yf.Ticker("^NSEI")
        return (ticker.news or [])[:10]
    except Exception:
        return []
