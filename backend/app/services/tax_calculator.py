import math
from datetime import datetime, timedelta
from typing import List, Dict


# ── Tax Calculator ────────────────────────────────────────────────────────────
LTCG_EXEMPTION   = 125000   # ₹1.25L (Budget 2024)
STCG_RATE        = 0.20     # 20% (post Jul 2024)
LTCG_RATE        = 0.125    # 12.5% (post Jul 2024)
LONG_TERM_DAYS   = 365


def classify_trade(gain: float, days: int) -> str:
    if gain >= 0:
        return "LTCG" if days > LONG_TERM_DAYS else "STCG"
    return "LTCL" if days > LONG_TERM_DAYS else "STCL"


def calculate_tax_summary(holdings: list) -> dict:
    stcg = ltcg = ltcl = stcl = 0.0
    trades = []

    for h in holdings:
        ltp = getattr(h, "_ltp", h.avg_price)
        gain = (ltp - h.avg_price) * h.qty

        try:
            buy_date = datetime.strptime(h.buy_date, "%Y-%m-%d") if h.buy_date else datetime.utcnow() - timedelta(days=400)
            days = (datetime.utcnow() - buy_date).days
        except (ValueError, TypeError):
            days = 400

        trade_type = classify_trade(gain, days)
        if trade_type == "STCG":   stcg += gain
        elif trade_type == "LTCG": ltcg += gain
        elif trade_type == "LTCL": ltcl += gain
        else:                      stcl += gain

        tax = (
            gain * STCG_RATE if trade_type == "STCG"
            else max(0, gain - LTCG_EXEMPTION) * LTCG_RATE if trade_type == "LTCG"
            else 0
        )
        trades.append({
            "symbol":        h.symbol,
            "buy_price":     h.avg_price,
            "current_price": round(ltp, 2),
            "qty":           h.qty,
            "gain":          round(gain, 2),
            "days":          days,
            "type":          trade_type,
            "tax":           round(tax, 2),
        })

    ltcg_exempt   = min(ltcg, LTCG_EXEMPTION)
    ltcg_taxable  = max(0, ltcg - ltcg_exempt)
    stcg_tax      = max(0, stcg) * STCG_RATE
    ltcg_tax      = ltcg_taxable * LTCG_RATE
    total_tax     = stcg_tax + ltcg_tax

    harvesting_tip = (
        f"You have ₹{abs(ltcl):,.0f} in long-term losses. Book them to save ₹{abs(ltcl) * LTCG_RATE:,.0f} in tax."
        if ltcl < -1000 else
        "No significant tax-loss harvesting opportunity currently."
    )

    return {
        "stcg":          round(stcg, 2),
        "ltcg":          round(ltcg, 2),
        "ltcl":          round(ltcl, 2),
        "stcl":          round(stcl, 2),
        "ltcg_exempt":   round(ltcg_exempt, 2),
        "ltcg_taxable":  round(ltcg_taxable, 2),
        "stcg_tax":      round(stcg_tax, 2),
        "ltcg_tax":      round(ltcg_tax, 2),
        "total_tax":     round(total_tax, 2),
        "trades":        trades,
        "tip":           harvesting_tip,
    }


# ── Goal Calculator ───────────────────────────────────────────────────────────
RETURN_RATES = {"Aggressive": 0.14, "Moderate": 0.12, "Conservative": 0.08}


def project_goal(saved: float, monthly: float, years: int, risk: str) -> dict:
    rate   = RETURN_RATES.get(risk, 0.12)
    months = years * 12
    r      = rate / 12

    fv_existing = saved * math.pow(1 + r, months)
    fv_sip      = monthly * ((math.pow(1 + r, months) - 1) / r) * (1 + r) if r > 0 else monthly * months
    projected   = fv_existing + fv_sip

    return {
        "projected":   round(projected, 2),
        "annual_rate": rate,
        "months":      months,
    }


def required_sip(target: float, saved: float, years: int, risk: str) -> float:
    """Calculate SIP needed to reach target."""
    rate   = RETURN_RATES.get(risk, 0.12)
    months = years * 12
    r      = rate / 12

    fv_existing = saved * math.pow(1 + r, months)
    remaining   = target - fv_existing
    if remaining <= 0:
        return 0.0

    sip = remaining * r / (((math.pow(1 + r, months) - 1) / r) * (1 + r)) if r > 0 else remaining / months
    return round(max(0, sip), 2)
