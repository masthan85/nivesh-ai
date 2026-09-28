from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

MONEY_QUANTUM = Decimal('0.01')
PERCENT_QUANTUM = Decimal('0.0001')


def D(value: Any) -> Decimal:
    """Convert values to Decimal without importing binary float artefacts."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def money(value: Any) -> Decimal:
    return D(value).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def percent(value: Any) -> Decimal:
    return D(value).quantize(PERCENT_QUANTUM, rounding=ROUND_HALF_UP)


def as_number(value: Decimal) -> float:
    """JSON boundary helper. Keep Decimal internally; convert only for legacy API compatibility."""
    return float(value)
