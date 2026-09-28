from pydantic import ValidationError
from app.schemas.user import UserCreate
from app.schemas.portfolio import BrokerCalcRequest, HoldingCreate
from app.services.broker_charges import calculate_charges


def test_weak_password_rejected():
    try:
        UserCreate(name='Test User', email='test@example.com', password='allletters')
        assert False, 'Expected password validation error'
    except ValidationError:
        pass


def test_invalid_holding_rejected():
    try:
        HoldingCreate(symbol='BAD SYMBOL!', name='Invalid', qty=-1, avg_price=0)
        assert False, 'Expected holding validation error'
    except ValidationError:
        pass


def test_broker_request_restricts_trade_type():
    try:
        BrokerCalcRequest(price=100, qty=10, trade_type='random')
        assert False, 'Expected trade type validation error'
    except ValidationError:
        pass


def test_broker_charge_is_deterministic_and_non_negative():
    result = calculate_charges('zerodha', 1000, 10, 'delivery')
    assert result['trade_value'] == 10000
    assert result['total'] >= 0
    assert result['pct_of_trade'] >= 0
