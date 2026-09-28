from decimal import Decimal
from types import SimpleNamespace
from app.services.tax_calculator import calculate_tax_summary, project_goal, required_sip


def test_tax_summary_uses_annual_ltcg_exemption_once():
    holdings = [
        SimpleNamespace(symbol='A', avg_price=Decimal('100'), qty=Decimal('1000'), buy_date='2020-01-01', _ltp=Decimal('200')),
        SimpleNamespace(symbol='B', avg_price=Decimal('100'), qty=Decimal('500'), buy_date='2020-01-01', _ltp=Decimal('200')),
    ]
    result = calculate_tax_summary(holdings)
    assert result['ltcg'] == 150000.0
    assert result['ltcg_exempt'] == 125000.0
    assert result['ltcg_taxable'] == 25000.0
    assert result['ltcg_tax'] == 3125.0


def test_goal_projection_and_required_sip_are_deterministic():
    a = project_goal(Decimal('100000'), Decimal('10000'), 5, 'Moderate')
    b = project_goal(Decimal('100000'), Decimal('10000'), 5, 'Moderate')
    assert a == b
    assert a['projected'] > 0
    assert required_sip(Decimal('1000000'), Decimal('100000'), 5, 'Moderate') >= 0
