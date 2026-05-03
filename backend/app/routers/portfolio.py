from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.schemas.portfolio import HoldingCreate, HoldingUpdate
from app.utils.auth import get_current_user
from app.services.market_data import get_live_price

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/holdings")
def get_holdings(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    result = []
    for h in holdings:
        ltp, chg = get_live_price(h.symbol)
        if ltp == 0:
            ltp = h.avg_price
        pnl     = (ltp - h.avg_price) * h.qty
        pnl_pct = (ltp - h.avg_price) / h.avg_price * 100 if h.avg_price else 0
        result.append({
            "id":             h.id,
            "symbol":         h.symbol,
            "name":           h.name,
            "qty":            h.qty,
            "avg_price":      h.avg_price,
            "sector":         h.sector,
            "exchange":       h.exchange,
            "asset_type":     h.asset_type,
            "buy_date":       h.buy_date,
            "ltp":            ltp,
            "change_pct":     round(chg, 2),
            "pnl":            round(pnl, 2),
            "pnl_pct":        round(pnl_pct, 2),
            "current_value":  round(ltp * h.qty, 2),
            "invested_value": round(h.avg_price * h.qty, 2),
        })
    return result


@router.get("/summary")
def get_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    total_invested = sum(h.avg_price * h.qty for h in holdings)
    total_current  = 0.0
    sector_map     = {}

    for h in holdings:
        ltp, _ = get_live_price(h.symbol)
        if ltp == 0:
            ltp = h.avg_price
        val = ltp * h.qty
        total_current += val
        sector_map[h.sector] = sector_map.get(h.sector, 0) + val

    gain     = total_current - total_invested
    gain_pct = gain / total_invested * 100 if total_invested else 0

    sectors = [
        {"name": k, "value": round(v, 2), "pct": round(v / total_current * 100, 1) if total_current else 0}
        for k, v in sector_map.items()
    ]
    sectors.sort(key=lambda x: -x["pct"])

    return {
        "total_invested":  round(total_invested, 2),
        "total_current":   round(total_current, 2),
        "total_gain":      round(gain, 2),
        "gain_pct":        round(gain_pct, 2),
        "holding_count":   len(holdings),
        "sectors":         sectors,
        "health_score":    min(100, max(40, round(60 + gain_pct * 0.5, 1))),
        "ai_score":        min(100, max(50, round(65 + gain_pct * 0.4, 1))),
    }


@router.post("/holdings", status_code=201)
def add_holding(data: HoldingCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = Holding(user_id=user.id, **data.dict())
    db.add(h)
    db.commit()
    db.refresh(h)
    return h


@router.put("/holdings/{holding_id}")
def update_holding(holding_id: int, data: HoldingUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == user.id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Holding not found")
    update_data = data.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(h, k, v)
    db.commit()
    db.refresh(h)
    return h


@router.delete("/holdings/{holding_id}")
def delete_holding(holding_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == user.id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(h)
    db.commit()
    return {"ok": True, "deleted_id": holding_id}
