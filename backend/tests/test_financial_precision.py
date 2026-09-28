from decimal import Decimal
from app.services.portfolio_calculator import holding_metrics, portfolio_totals
from app.services.broker_charges import calculate_charges
from app.providers.market_data import UnavailableMarketDataProvider


def test_holding_metrics_are_precision_safe():
    result = holding_metrics(Decimal('0.1'), Decimal('0.1'), Decimal('0.3'))
    assert result['invested_value'] == 0.01
    assert result['current_value'] == 0.03
    assert result['pnl'] == 0.02
    assert result['pnl_pct'] == 200.0


def test_portfolio_totals_do_not_accumulate_float_error():
    rows = [
        (Decimal('0.1'), Decimal('0.1'), Decimal('0.3')),
        (Decimal('0.2'), Decimal('0.2'), Decimal('0.4')),
    ]
    result = portfolio_totals(rows)
    assert result['total_invested'] == 0.05
    assert result['total_current'] == 0.11
    assert result['total_gain'] == 0.06


def test_broker_calculator_rejects_unknown_broker():
    try:
        calculate_charges('unknown', Decimal('100'), 1, 'delivery')
        assert False, 'expected ValueError'
    except ValueError:
        pass


def test_unavailable_provider_never_fabricates_price():
    quote = UnavailableMarketDataProvider().get_quote('TEST')
    assert quote.price is None
    assert quote.is_live is False
    assert quote.freshness == 'unavailable'
