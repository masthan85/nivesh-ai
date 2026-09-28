from __future__ import annotations
from decimal import Decimal
from app.domain.money import D, money, percent, as_number


def holding_metrics(quantity, average_price, current_price) -> dict:
    qty = D(quantity)
    avg = D(average_price)
    current = D(current_price)
    invested = avg * qty
    value = current * qty
    pnl = value - invested
    pnl_pct = Decimal('0') if invested == 0 else pnl / invested * D('100')
    return {
        'current_value': as_number(money(value)),
        'invested_value': as_number(money(invested)),
        'pnl': as_number(money(pnl)),
        'pnl_pct': as_number(percent(pnl_pct)),
    }


def portfolio_totals(rows: list[tuple]) -> dict:
    invested = sum((D(avg) * D(qty) for qty, avg, _ in rows), Decimal('0'))
    current = sum((D(price) * D(qty) for qty, _, price in rows), Decimal('0'))
    gain = current - invested
    gain_pct = Decimal('0') if invested == 0 else gain / invested * D('100')
    return {
        'total_invested': as_number(money(invested)),
        'total_current': as_number(money(current)),
        'total_gain': as_number(money(gain)),
        'gain_pct': as_number(percent(gain_pct)),
    }
