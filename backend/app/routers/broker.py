from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query

from app.schemas.portfolio import BrokerCalcRequest, TradeType
from app.services.broker_charges import BROKER_RATES, calculate_charges, compare_all_brokers

router = APIRouter(prefix="/broker", tags=["Broker Costs"])


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
