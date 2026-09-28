from __future__ import annotations
from decimal import Decimal
from typing import Dict
from app.domain.money import D, money, percent, as_number

BROKER_RATES: Dict[str, dict] = {
    'zerodha': {'name': 'Zerodha', 'delivery': '0', 'intraday': '0.0003', 'fo': '20', 'min': '0', 'note': 'Illustrative rate card; verify against current broker tariff.'},
    'groww': {'name': 'Groww', 'delivery': '0', 'intraday': '0.0005', 'fo': '20', 'min': '0', 'note': 'Illustrative rate card; verify against current broker tariff.'},
    'angelone': {'name': 'Angel One', 'delivery': '0', 'intraday': '0.0025', 'fo': '20', 'min': '0', 'note': 'Illustrative rate card; verify against current broker tariff.'},
    'upstox': {'name': 'Upstox', 'delivery': '0', 'intraday': '0.0005', 'fo': '20', 'min': '0', 'note': 'Illustrative rate card; verify against current broker tariff.'},
    'dhan': {'name': 'Dhan', 'delivery': '0', 'intraday': '0.0003', 'fo': '20', 'min': '0', 'note': 'Illustrative rate card; verify against current broker tariff.'},
}


def _fee(rate: Decimal, minimum: Decimal, trade_value: Decimal, trade_type: str) -> Decimal:
    if rate == 0:
        return Decimal('0')
    if rate >= 1:
        return rate
    raw = trade_value * rate
    return max(minimum, raw if trade_type == 'delivery' else min(Decimal('20'), raw))


def calculate_charges(broker_id: str, price, qty: int, trade_type: str) -> dict:
    if broker_id not in BROKER_RATES:
        raise ValueError('Unknown broker')
    if trade_type not in {'delivery', 'intraday', 'fo'}:
        raise ValueError('Unsupported trade type')

    b = BROKER_RATES[broker_id]
    trade_value = D(price) * D(qty)
    brokerage = _fee(D(b[trade_type]), D(b['min']), trade_value, trade_type)

    stt_rate = {'delivery': D('0.001'), 'intraday': D('0.00025'), 'fo': D('0.0005')}[trade_type]
    stamp_rate = {'delivery': D('0.00015'), 'intraday': D('0.00003'), 'fo': D('0.00002')}[trade_type]
    stt = trade_value * stt_rate
    exchange = trade_value * D('0.0000325')
    sebi = trade_value * D('0.000001')
    stamp = trade_value * stamp_rate
    dp_charges = D('13.50') if trade_type == 'delivery' else D('0')
    gst = (brokerage + exchange) * D('0.18')
    total = brokerage + stt + exchange + sebi + stamp + dp_charges + gst
    pct = Decimal('0') if trade_value == 0 else total / trade_value * D('100')

    return {
        'broker_id': broker_id,
        'broker_name': b['name'],
        'note': b['note'],
        'brokerage': as_number(money(brokerage)),
        'stt': as_number(money(stt)),
        'exchange_txn': as_number(money(exchange)),
        'sebi': as_number(sebi.quantize(Decimal('0.0001'))),
        'stamp_duty': as_number(money(stamp)),
        'dp_charges': as_number(money(dp_charges)),
        'gst': as_number(money(gst)),
        'total': as_number(money(total)),
        'trade_value': as_number(money(trade_value)),
        'pct_of_trade': as_number(percent(pct)),
        'calculation_status': 'illustrative-unverified',
    }


def compare_all_brokers(price, qty: int, trade_type: str) -> dict:
    results = [calculate_charges(bid, price, qty, trade_type) for bid in BROKER_RATES]
    results.sort(key=lambda x: x['total'])
    return {
        'results': results,
        'cheapest': results[0]['broker_id'],
        'most_expensive': results[-1]['broker_id'],
        'max_savings': as_number(money(D(results[-1]['total']) - D(results[0]['total']))),
        'disclaimer': 'Illustrative comparison only. Broker tariffs and statutory charges must be verified against current authoritative sources before production use.',
    }
