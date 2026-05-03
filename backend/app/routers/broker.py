from fastapi import APIRouter
from app.schemas.portfolio import BrokerCalcRequest
from app.services.broker_charges import compare_all_brokers, calculate_charges

router = APIRouter(prefix="/broker", tags=["Broker Costs"])


@router.post("/calculate")
def calculate_broker_costs(req: BrokerCalcRequest):
    return compare_all_brokers(req.price, req.qty, req.trade_type)


@router.get("/charges/{broker_id}")
def single_broker_charges(broker_id: str, price: float, qty: int, trade_type: str = "delivery"):
    return calculate_charges(broker_id, price, qty, trade_type)
