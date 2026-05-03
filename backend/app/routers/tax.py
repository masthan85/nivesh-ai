"""routers/tax.py"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.utils.auth import get_current_user
from app.services.market_data import get_live_price
from app.services.tax_calculator import calculate_tax_summary

router = APIRouter(prefix="/tax", tags=["Tax P&L"])


@router.get("/summary")
def tax_summary(fy: str = "2025-26", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    # Attach live prices to holdings for calculation
    for h in holdings:
        ltp, _ = get_live_price(h.symbol)
        h._ltp = ltp if ltp > 0 else h.avg_price
    result = calculate_tax_summary(holdings)
    result["fy"] = fy
    return result
