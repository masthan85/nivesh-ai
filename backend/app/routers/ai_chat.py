from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding, ChatMessage
from app.schemas.portfolio import ChatRequest
from app.utils.auth import get_current_user
from app.config import settings

router = APIRouter(prefix='/ai', tags=['Nia AI'])

@router.post('/chat')
async def ai_chat(req: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(status_code=503, detail='Nia AI provider is not configured for this environment')

    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    portfolio_ctx = ', '.join([f'{h.symbol}({h.qty}@₹{h.avg_price})' for h in holdings]) or 'No holdings'
    system_prompt = f'''You are Nia, the investment-intelligence assistant inside Nivara AI.

User context (authorised application data):
Risk profile: {user.risk}
Investment horizon: {user.horizon} years
Monthly SIP budget: ₹{user.monthly_sip:,.0f}
Portfolio holdings: {portfolio_ctx}

Safety and quality rules:
1. Never invent prices, fundamentals, news, events, sources, citations, or confidence percentages.
2. Treat portfolio quantities and costs above as user-provided application data, not live market data.
3. If a question requires current external information and none is supplied in the conversation, say that current verified data is unavailable.
4. Separate deterministic portfolio facts from interpretation.
5. Do not claim to be a regulated financial adviser and do not promise returns.
6. Keep responses concise and state material uncertainty.
7. End with: "AI-assisted research only — not certified financial advice."
'''
    messages = req.history[-10:] + [{'role': 'user', 'content': req.message}]
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=5.0)) as client:
            resp = await client.post(
                'https://api.anthropic.com/v1/messages',
                headers={'x-api-key': settings.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
                json={'model': 'claude-sonnet-4-20250514', 'max_tokens': 1000, 'system': system_prompt, 'messages': messages},
            )
            resp.raise_for_status()
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail='Nia AI provider timed out') from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail='Nia AI provider is temporarily unavailable') from exc

    data = resp.json()
    content = data.get('content') or []
    reply = next((item.get('text') for item in content if item.get('type') == 'text' and item.get('text')), None)
    if not reply:
        raise HTTPException(status_code=502, detail='Nia AI provider returned an invalid response')

    db.add(ChatMessage(user_id=user.id, role='user', content=req.message))
    db.add(ChatMessage(user_id=user.id, role='assistant', content=reply))
    db.commit()
    return {'reply': reply, 'grounding': 'portfolio-context-only', 'live_external_data': False}

@router.get('/history')
def chat_history(limit: int = 20, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    msgs = db.query(ChatMessage).filter(ChatMessage.user_id == user.id).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    return [{'role': m.role, 'content': m.content, 'created_at': m.created_at.isoformat()} for m in reversed(msgs)]
