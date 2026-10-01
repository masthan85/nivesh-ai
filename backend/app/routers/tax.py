"""Hypothetical capital-gains illustration on unrealised holdings.

Scope is deliberately narrow: listed equity and equity ETFs, using the current quote as a
hypothetical sale price. Holdings without a quote, and other asset types, are excluded and
listed rather than silently valued at cost. This is not a filing-ready computation.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.portfolio import Holding
from app.models.user import User
from app.services.market_data import get_quote
from app.services.tax_calculator import calculate_tax_summary
from app.utils.auth import get_current_user

router = APIRouter(prefix="/tax", tags=["Tax P&L"])

IN_SCOPE_ASSET_TYPES = {"Equity", "ETF"}


@router.get("/summary")
def tax_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    included, excluded = [], []
    for h in holdings:
        if h.asset_type not in IN_SCOPE_ASSET_TYPES:
            excluded.append({"symbol": h.symbol, "reason": f"Asset type {h.asset_type} is not covered yet"})
            continue
        quote = get_quote(h.symbol)
        if quote.price is None:
            excluded.append({"symbol": h.symbol, "reason": "No current quote available"})
            continue
        h._ltp = quote.price
        included.append(h)

    result = calculate_tax_summary(included)
    result.update({
        "basis": "hypothetical-sale-of-unrealised-holdings-at-current-quote",
        "scope": "Listed equity and equity ETFs only",
        "excluded": excluded,
        "not_covered": [
            "Realised transactions during the year",
            "Set-off and carry-forward of losses",
            "Grandfathering of pre-February-2018 acquisition cost",
            "Debt, hybrid and international funds",
        ],
    })
    return result
