"""routers/ai_chat.py"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import httpx
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding, ChatMessage
from app.schemas.portfolio import ChatRequest
from app.utils.auth import get_current_user
from app.config import settings

router = APIRouter(prefix="/ai", tags=["AI Advisor"])


@router.post("/chat")
async def ai_chat(req: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not settings.ANTHROPIC_API_KEY:
        return {"reply": "⚠️ ANTHROPIC_API_KEY not configured. Add it to backend/.env"}

    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()
    portfolio_ctx = ", ".join([f"{h.symbol}({h.qty}@₹{h.avg_price})" for h in holdings]) or "No holdings yet"

    system_prompt = f"""You are Nivesh AI (nivesh = investment in Hindi), an expert investment intelligence advisor built specifically for Indian markets.

User Profile:
- Name: {user.name}
- Risk Profile: {user.risk}
- Investment Horizon: {user.horizon} years  
- Monthly SIP Budget: ₹{user.monthly_sip:,.0f}

Current Portfolio: {portfolio_ctx}

Guidelines:
- Give concise, data-driven advice specific to Indian markets (NSE/BSE)
- Reference the user's actual holdings when relevant
- Use bullet points for recommendations
- Include confidence scores (e.g., "Confidence: 78%")
- Cite technical/fundamental reasoning briefly
- Always end with: "⚠️ AI-assisted insights only — not certified financial advice."
"""

    messages = req.history[-10:] + [{"role": "user", "content": req.message}]

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "system": system_prompt,
                "messages": messages,
            }
        )

    data = resp.json()
    reply = data.get("content", [{}])[0].get("text", "Unable to process. Please try again.")

    # Save to history
    db.add(ChatMessage(user_id=user.id, role="user",      content=req.message))
    db.add(ChatMessage(user_id=user.id, role="assistant", content=reply))
    db.commit()

    return {"reply": reply}


@router.get("/history")
def chat_history(limit: int = 20, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    msgs = db.query(ChatMessage).filter(ChatMessage.user_id == user.id).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    return [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in reversed(msgs)]
