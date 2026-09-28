from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.goal import WatchItem, PriceAlert
from app.schemas.portfolio import WatchCreate, AlertCreate
from app.utils.auth import get_current_user
from app.services.market_data import get_quote

watchlist_router = APIRouter(prefix="/watchlist", tags=["Watchlist"])
alerts_router    = APIRouter(prefix="/alerts",    tags=["Price Alerts"])


# ── Watchlist ─────────────────────────────────────────────────────────────────
@watchlist_router.get("/")
def get_watchlist(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(WatchItem).filter(WatchItem.user_id == user.id).all()
    result = []
    for w in items:
        quote = get_quote(w.symbol)
        prev = quote.previous_close or quote.price
        chg = 0.0 if quote.price is None or prev in (None, 0) else float((quote.price - prev) / prev * 100)
        result.append({
            "id":        w.id,
            "symbol":    w.symbol,
            "target":    float(w.target) if w.target is not None else None,
            "stop_loss": float(w.stop_loss) if w.stop_loss is not None else None,
            "notes":     w.notes,
            "ltp":       float(quote.price) if quote.price is not None else None,
            "change_pct":chg,
            "added_at":  w.added_at.isoformat() if w.added_at else "",
            "market_data": {"source": quote.source, "as_of": quote.as_of.isoformat(), "freshness": quote.freshness, "is_live": quote.is_live},
        })
    return result


@watchlist_router.post("/", status_code=201)
def add_to_watchlist(data: WatchCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(WatchItem).filter(WatchItem.user_id == user.id, WatchItem.symbol == data.symbol.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Symbol already in watchlist")
    w = WatchItem(user_id=user.id, symbol=data.symbol.upper(), target=data.target, stop_loss=data.stop_loss, notes=data.notes)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


@watchlist_router.delete("/{item_id}")
def remove_from_watchlist(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.query(WatchItem).filter(WatchItem.id == item_id, WatchItem.user_id == user.id).first()
    if not w:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(w)
    db.commit()
    return {"ok": True}


# ── Price Alerts ──────────────────────────────────────────────────────────────
@alerts_router.get("/")
def get_alerts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(PriceAlert).filter(PriceAlert.user_id == user.id).all()


@alerts_router.post("/", status_code=201)
def create_alert(data: AlertCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = PriceAlert(user_id=user.id, **data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@alerts_router.delete("/{alert_id}")
def delete_alert(alert_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.query(PriceAlert).filter(PriceAlert.id == alert_id, PriceAlert.user_id == user.id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(a)
    db.commit()
    return {"ok": True}
