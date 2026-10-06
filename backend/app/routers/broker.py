from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.broker_connection import GrowwConnectRequest
from app.schemas.portfolio import BrokerCalcRequest, TradeType
from app.services.audit import record_audit_event
from app.services.broker_charges import BROKER_RATES, calculate_charges, compare_all_brokers
from app.services.broker_connections import (
    BrokerConnectionError,
    fetch_groww_snapshot,
    motilal_login_url,
    provider_catalog,
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/broker", tags=["Broker Connections & Costs"])


@router.get("/providers")
def providers():
    """Connection capabilities only; no credentials or private account data."""
    return {"providers": provider_catalog()}


@router.post("/connect/groww/preview")
def connect_groww_preview(
    req: GrowwConnectRequest,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verify a Groww user token and return a read-only account snapshot.

    The access token is deliberately not persisted by Nivara in this implementation.
    """
    try:
        snapshot = fetch_groww_snapshot(req.access_token)
    except BrokerConnectionError as exc:
        record_audit_event(
            db,
            "broker.groww.connect",
            user_id=user.id,
            outcome="failure",
            request_id=getattr(request.state, "request_id", None),
            ip_address=request.client.host if request.client else None,
            metadata={"reason": str(exc)},
        )
        db.commit()
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    record_audit_event(
        db,
        "broker.groww.connect",
        user_id=user.id,
        request_id=getattr(request.state, "request_id", None),
        ip_address=request.client.host if request.client else None,
        metadata={"provider": "groww", "holding_count": snapshot["holding_count"], "persisted_token": False},
    )
    db.commit()
    return snapshot


@router.get("/connect/motilal-oswal")
def connect_motilal_oswal(user: User = Depends(get_current_user)):
    """Return the official MOFSL broker-login URL when Nivara's API app key is configured."""
    url = motilal_login_url()
    if not url:
        raise HTTPException(
            status_code=503,
            detail="Motilal Oswal connector needs MOTILAL_API_KEY and a broker-registered Nivara redirect URL before login can be completed.",
        )
    return {
        "provider": "motilal-oswal",
        "authorization_url": url,
        "status": "redirect_ready",
        "notice": "Authentication happens on Motilal Oswal. Nivara must never collect the broker password.",
    }


@router.post("/calculate")
def calculate_broker_costs(req: BrokerCalcRequest):
    return compare_all_brokers(req.price, req.qty, req.trade_type)


@router.get("/charges/{broker_id}")
def single_broker_charges(
    broker_id: str,
    price: Decimal = Query(gt=0, max_digits=24, decimal_places=4),
    qty: int = Query(gt=0, le=10_000_000),
    trade_type: TradeType = "delivery",
):
    if broker_id not in BROKER_RATES:
        raise HTTPException(status_code=404, detail="Unknown broker")
    return calculate_charges(broker_id, price, qty, trade_type)
