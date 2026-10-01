from __future__ import annotations
from datetime import datetime, timedelta, timezone
from decimal import Decimal, getcontext
from app.domain.money import D, money, as_number

getcontext().prec = 34

LTCG_EXEMPTION = D('125000')
STCG_RATE = D('0.20')
LTCG_RATE = D('0.125')
LONG_TERM_DAYS = 365
RETURN_RATES = {'Aggressive': D('0.14'), 'Moderate': D('0.12'), 'Conservative': D('0.08')}


def classify_trade(gain, days: int) -> str:
    gain = D(gain)
    if gain >= 0:
        return 'LTCG' if days > LONG_TERM_DAYS else 'STCG'
    return 'LTCL' if days > LONG_TERM_DAYS else 'STCL'


def calculate_tax_summary(holdings: list) -> dict:
    stcg = ltcg = ltcl = stcl = D('0')
    trades = []
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for holding in holdings:
        ltp = D(getattr(holding, '_ltp', holding.avg_price))
        avg = D(holding.avg_price)
        qty = D(holding.qty)
        gain = (ltp - avg) * qty
        try:
            buy_date = datetime.strptime(holding.buy_date, '%Y-%m-%d') if holding.buy_date else now - timedelta(days=400)
            days = (now - buy_date).days
        except (ValueError, TypeError):
            days = 400
        trade_type = classify_trade(gain, days)
        if trade_type == 'STCG': stcg += gain
        elif trade_type == 'LTCG': ltcg += gain
        elif trade_type == 'LTCL': ltcl += gain
        else: stcl += gain

        # Per-holding tax is indicative only; the portfolio summary applies the annual exemption once.
        indicative_tax = gain * STCG_RATE if trade_type == 'STCG' and gain > 0 else D('0')
        trades.append({
            'symbol': holding.symbol,
            'buy_price': as_number(money(avg)),
            'current_price': as_number(money(ltp)),
            'qty': float(qty),
            'gain': as_number(money(gain)),
            'days': days,
            'type': trade_type,
            'indicative_tax_before_annual_adjustments': as_number(money(indicative_tax)),
        })

    ltcg_exempt = min(max(ltcg, D('0')), LTCG_EXEMPTION)
    ltcg_taxable = max(D('0'), ltcg - ltcg_exempt)
    stcg_tax = max(D('0'), stcg) * STCG_RATE
    ltcg_tax = ltcg_taxable * LTCG_RATE
    total_tax = stcg_tax + ltcg_tax

    return {
        'stcg': as_number(money(stcg)),
        'ltcg': as_number(money(ltcg)),
        'ltcl': as_number(money(ltcl)),
        'stcl': as_number(money(stcl)),
        'ltcg_exempt': as_number(money(ltcg_exempt)),
        'ltcg_taxable': as_number(money(ltcg_taxable)),
        'stcg_tax': as_number(money(stcg_tax)),
        'ltcg_tax': as_number(money(ltcg_tax)),
        'total_tax': as_number(money(total_tax)),
        'trades': trades,
        'calculation_status': 'hypothetical-illustration-rules-require-current-validation',
        'disclaimer': 'Hypothetical illustration only, not a filing-ready computation. Tax treatment depends on instrument, transaction dates, residency and current law.',
    }


def _compound(base: Decimal, exponent: int) -> Decimal:
    return base ** exponent


def project_goal(saved, monthly, years: int, risk: str) -> dict:
    annual_rate = RETURN_RATES.get(risk, D('0.12'))
    months = years * 12
    monthly_rate = annual_rate / D('12')
    factor = _compound(D('1') + monthly_rate, months)
    fv_existing = D(saved) * factor
    if monthly_rate > 0:
        fv_sip = D(monthly) * ((factor - D('1')) / monthly_rate) * (D('1') + monthly_rate)
    else:
        fv_sip = D(monthly) * D(months)
    projected = fv_existing + fv_sip
    return {'projected': as_number(money(projected)), 'annual_rate': float(annual_rate), 'months': months}


def required_sip(target, saved, years: int, risk: str) -> float:
    annual_rate = RETURN_RATES.get(risk, D('0.12'))
    months = years * 12
    monthly_rate = annual_rate / D('12')
    factor = _compound(D('1') + monthly_rate, months)
    fv_existing = D(saved) * factor
    remaining = D(target) - fv_existing
    if remaining <= 0:
        return 0.0
    if monthly_rate > 0:
        denominator = ((factor - D('1')) / monthly_rate) * (D('1') + monthly_rate)
        sip = remaining / denominator
    else:
        sip = remaining / D(months)
    return as_number(money(max(D('0'), sip)))
