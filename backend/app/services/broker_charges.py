from typing import Dict, List

BROKER_RATES: Dict[str, dict] = {
    "zerodha":    {"name": "Zerodha",          "logo": "🔷", "delivery": 0,      "intraday": 0.0003,  "fo": 20,   "min": 0,  "note": "₹20 cap intraday · Zero delivery"},
    "groww":      {"name": "Groww",            "logo": "🌱", "delivery": 0,      "intraday": 0.0005,  "fo": 20,   "min": 0,  "note": "₹20 cap intraday · Zero delivery"},
    "angelone":   {"name": "Angel One",        "logo": "😇", "delivery": 0,      "intraday": 0.0025,  "fo": 20,   "min": 0,  "note": "₹20 cap · Zero delivery"},
    "upstox":     {"name": "Upstox",           "logo": "⬆️", "delivery": 0,      "intraday": 0.0005,  "fo": 20,   "min": 0,  "note": "₹20 cap · Zero delivery"},
    "dhan":       {"name": "Dhan",             "logo": "💎", "delivery": 0,      "intraday": 0.0003,  "fo": 20,   "min": 0,  "note": "₹20 cap · Zero delivery"},
    "fyers":      {"name": "Fyers",            "logo": "🦅", "delivery": 0,      "intraday": 0.0003,  "fo": 20,   "min": 0,  "note": "₹20 cap · Free delivery"},
    "5paisa":     {"name": "5Paisa",           "logo": "5️⃣", "delivery": 20,     "intraday": 20,      "fo": 20,   "min": 20, "note": "Flat ₹20 per order"},
    "icicidirect":{"name": "ICICI Direct",     "logo": "🏦", "delivery": 0.0055, "intraday": 0.00275, "fo": 0.0005,"min":35, "note": "0.55% delivery · Min ₹35"},
    "hdfc":       {"name": "HDFC Securities",  "logo": "🔴", "delivery": 0.005,  "intraday": 0.0025,  "fo": 100,  "min": 25, "note": "0.50% delivery · Min ₹25"},
    "motilaloswal":{"name":"Motilal Oswal",    "logo": "🦁", "delivery": 0.005,  "intraday": 0.0005,  "fo": 20,   "min": 0,  "note": "0.50% delivery · ₹20 intraday"},
    "sharekhan":  {"name": "Sharekhan",        "logo": "🦈", "delivery": 0.005,  "intraday": 0.001,   "fo": 100,  "min": 0,  "note": "0.50% delivery · 0.10% intraday"},
    "kotak":      {"name": "Kotak Neo",        "logo": "🔵", "delivery": 0,      "intraday": 0.0003,  "fo": 20,   "min": 0,  "note": "Zero delivery · ₹20 intraday"},
    "axisdirect": {"name": "Axis Direct",      "logo": "🟣", "delivery": 0.005,  "intraday": 0.0025,  "fo": 20,   "min": 30, "note": "0.50% delivery · ₹30 min"},
    "sbisec":     {"name": "SBI Securities",   "logo": "🏛️", "delivery": 0.005,  "intraday": 0.0025,  "fo": 100,  "min": 0,  "note": "0.50% delivery"},
    "samco":      {"name": "SAMCO",            "logo": "📈", "delivery": 0,      "intraday": 0.0003,  "fo": 20,   "min": 0,  "note": "₹20 cap · Zero delivery"},
}


def calculate_charges(broker_id: str, price: float, qty: int, trade_type: str) -> dict:
    """Calculate all-in charges for a broker trade."""
    b = BROKER_RATES.get(broker_id, BROKER_RATES["zerodha"])
    trade_val = price * qty
    rate = b.get(trade_type, b["delivery"])

    if rate == 0:
        brokerage = 0.0
    elif rate >= 1:
        # flat fee
        brokerage = float(rate)
    else:
        # percentage — cap at ₹20 for intraday/fo
        raw = trade_val * rate
        if trade_type == "delivery":
            brokerage = max(float(b["min"]), raw)
        else:
            brokerage = max(float(b["min"]), min(20.0, raw))

    # Regulatory charges (same for all brokers)
    stt        = trade_val * (0.001 if trade_type == "delivery" else 0.00025 if trade_type == "intraday" else 0.0005)
    exchange   = trade_val * 0.0000325   # NSE transaction charge
    sebi       = trade_val * 0.000001    # SEBI turnover fee
    stamp      = trade_val * (0.00015 if trade_type == "delivery" else 0.00003)
    dp_charges = 13.5 if trade_type == "delivery" else 0.0   # DP charges on sell
    gst        = (brokerage + exchange) * 0.18

    total = brokerage + stt + exchange + sebi + stamp + dp_charges + gst

    return {
        "broker_id":    broker_id,
        "broker_name":  b["name"],
        "logo":         b["logo"],
        "note":         b["note"],
        "brokerage":    round(brokerage, 2),
        "stt":          round(stt, 2),
        "exchange_txn": round(exchange, 2),
        "sebi":         round(sebi, 4),
        "stamp_duty":   round(stamp, 2),
        "dp_charges":   round(dp_charges, 2),
        "gst":          round(gst, 2),
        "total":        round(total, 2),
        "trade_value":  round(trade_val, 2),
        "pct_of_trade": round(total / trade_val * 100, 4) if trade_val else 0,
    }


def compare_all_brokers(price: float, qty: int, trade_type: str) -> dict:
    """Compare charges across all brokers, sorted by total cost."""
    results = [calculate_charges(bid, price, qty, trade_type) for bid in BROKER_RATES]
    results.sort(key=lambda x: x["total"])
    return {
        "results":       results,
        "cheapest":      results[0]["broker_id"],
        "most_expensive":results[-1]["broker_id"],
        "max_savings":   round(results[-1]["total"] - results[0]["total"], 2),
    }
