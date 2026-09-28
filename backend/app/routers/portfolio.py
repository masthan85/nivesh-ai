from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.schemas.portfolio import HoldingCreate, HoldingUpdate
from app.utils.auth import get_current_user
from app.services.market_data import get_quote
from app.services.portfolio_calculator import holding_metrics, portfolio_totals

router = APIRouter(prefix='/portfolio', tags=['Portfolio'])


def _effective_price(holding, quote):
    if quote.price is not None:
        return quote.price, quote
    return Decimal(str(holding.avg_price)), quote


@router.get('/holdings')
def get_holdings(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    result = []
    for h in holdings:
        quote = get_quote(h.symbol)
        price, quote = _effective_price(h, quote)
        metrics = holding_metrics(h.qty, h.avg_price, price)
        previous = quote.previous_close or price
        change_pct = Decimal('0') if previous == 0 else (price - previous) / previous * Decimal('100')
        result.append({
            'id': h.id,
            'symbol': h.symbol,
            'name': h.name,
            'qty': float(h.qty),
            'avg_price': float(h.avg_price),
            'sector': h.sector,
            'exchange': h.exchange,
            'asset_type': h.asset_type,
            'buy_date': h.buy_date,
            'ltp': float(price),
            'change_pct': float(change_pct.quantize(Decimal('0.01'))),
            **metrics,
            'market_data': {
                'source': quote.source,
                'as_of': quote.as_of.isoformat(),
                'freshness': quote.freshness,
                'is_live': quote.is_live,
                'fallback_to_cost': quote.price is None,
            },
        })
    return result


@router.get('/summary')
def get_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    rows = []
    sector_values: dict[str, Decimal] = {}
    unavailable_symbols = []
    for h in holdings:
        quote = get_quote(h.symbol)
        price, _ = _effective_price(h, quote)
        if quote.price is None:
            unavailable_symbols.append(h.symbol)
        rows.append((h.qty, h.avg_price, price))
        value = Decimal(str(price)) * Decimal(str(h.qty))
        sector_values[h.sector] = sector_values.get(h.sector, Decimal('0')) + value

    totals = portfolio_totals(rows)
    current = Decimal(str(totals['total_current']))
    sectors = []
    for name, value in sector_values.items():
        pct = Decimal('0') if current == 0 else value / current * Decimal('100')
        sectors.append({'name': name, 'value': float(value.quantize(Decimal('0.01'))), 'pct': float(pct.quantize(Decimal('0.1')))})
    sectors.sort(key=lambda x: -x['pct'])

    return {
        **totals,
        'holding_count': len(holdings),
        'sectors': sectors,
        'market_data_complete': not unavailable_symbols,
        'unavailable_symbols': unavailable_symbols,
        'valuation_note': 'When market data is unavailable, cost basis is used only as an explicit fallback and is not represented as a live valuation.' if unavailable_symbols else None,
    }


@router.post('/holdings', status_code=201)
def add_holding(data: HoldingCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = Holding(user_id=user.id, **data.model_dump())
    db.add(h)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Holding already exists for this symbol and exchange')
    db.refresh(h)
    return h


@router.put('/holdings/{holding_id}')
def update_holding(holding_id: int, data: HoldingUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == user.id).first()
    if not h:
        raise HTTPException(status_code=404, detail='Holding not found')
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(h, key, value)
    db.commit()
    db.refresh(h)
    return h


@router.delete('/holdings/{holding_id}')
def delete_holding(holding_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == user.id).first()
    if not h:
        raise HTTPException(status_code=404, detail='Holding not found')
    db.delete(h)
    db.commit()
    return {'ok': True, 'deleted_id': holding_id}
