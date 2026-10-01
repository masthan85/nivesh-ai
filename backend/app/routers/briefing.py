"""Daily briefing.

Reports only what the application can support with data: the user's holdings and the
quotes the configured provider returns, each with source and freshness. Index levels,
market mood and event calendars are not included until a licensed source provides them.
The briefing describes moves; it does not tell the user what to do about them.
"""
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.money import percent
from app.models.portfolio import Holding
from app.models.user import User
from app.services.market_data import get_quote
from app.utils.auth import get_current_user

router = APIRouter(prefix="/briefing", tags=["Daily Briefing"])

NOTABLE_MOVE_PCT = Decimal("1.5")


@router.get("/daily")
def daily_briefing(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    movers, unavailable, sources = [], [], set()

    for h in holdings:
        quote = get_quote(h.symbol)
        sources.add(quote.source)
        if quote.price is None or not quote.previous_close:
            unavailable.append(h.symbol)
            continue
        change_pct = percent((quote.price - quote.previous_close) / quote.previous_close * Decimal("100"))
        if abs(change_pct) >= NOTABLE_MOVE_PCT:
            movers.append({
                "symbol": h.symbol,
                "change_pct": float(change_pct),
                "price": float(quote.price),
                "source": quote.source,
                "as_of": quote.as_of.isoformat(),
                "freshness": quote.freshness,
            })

    movers.sort(key=lambda m: -abs(m["change_pct"]))
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "holding_count": len(holdings),
        "notable_moves": movers[:5],
        "notable_move_threshold_pct": float(NOTABLE_MOVE_PCT),
        "unavailable_symbols": unavailable,
        "data_sources": sorted(sources),
        "market_overview": {"status": "unavailable", "reason": "No licensed index or market-calendar source is configured."},
        "note": "Moves are reported for information only and are not recommendations.",
    }
