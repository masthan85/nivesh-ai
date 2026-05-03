"""routers/briefing.py — Daily AI briefing"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.utils.auth import get_current_user
from app.services.market_data import get_live_price

router = APIRouter(prefix="/briefing", tags=["Daily Briefing"])


@router.get("/daily")
def daily_briefing(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    alerts      = []
    top_movers  = []

    for h in holdings:
        ltp, chg = get_live_price(h.symbol)
        if ltp == 0:
            ltp = h.avg_price
        if abs(chg) > 1.5:
            top_movers.append({"symbol": h.symbol, "change_pct": chg, "ltp": ltp})
        if chg < -3:
            alerts.append({"type": "danger",  "msg": f"{h.symbol} is down {abs(chg):.1f}% today. Review your position."})
        elif chg > 3:
            alerts.append({"type": "success", "msg": f"{h.symbol} is up {chg:.1f}% today. Consider booking partial profits."})

    top_movers.sort(key=lambda x: -abs(x["change_pct"]))

    return {
        "date":         datetime.now().strftime("%A, %B %d, %Y"),
        "greeting":     f"Good morning, {user.name}!",
        "market_mood":  "Bullish",
        "nifty":        {"value": 22847, "change": 0.43},
        "sensex":       {"value": 75200, "change": 0.38},
        "vix":          16.2,
        "alerts":       alerts,
        "top_movers":   top_movers[:5],
        "ai_tip":       f"Focus on your {top_movers[0]['symbol'] if top_movers else 'SIP contributions'} today.",
        "upcoming_events": [
            {"date": "May 5",  "event": "Nifty F&O Expiry",    "type": "info"},
            {"date": "May 8",  "event": "RBI Policy Meeting",   "type": "warn"},
            {"date": "May 12", "event": "US CPI Data Release",  "type": "warn"},
            {"date": "May 15", "event": "INFY Q1 Results",      "type": "info"},
        ]
    }
