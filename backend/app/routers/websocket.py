"""Price stream for the authenticated user's own holdings.

Browsers cannot set Authorization headers on WebSocket connections, so the access token is
sent as the first message: {"type": "auth", "token": "..."}. Keeping it out of the URL keeps
it out of proxy and server access logs.
"""
import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from starlette.concurrency import run_in_threadpool

from app.database import SessionLocal
from app.models.portfolio import Holding
from app.services.market_data import get_quote
from app.utils.auth import user_from_token

ws_router = APIRouter(tags=["WebSocket"])

AUTH_TIMEOUT_SECONDS = 10
INTERVAL_SECONDS = 15
MAX_SYMBOLS = 25
POLICY_VIOLATION = 1008


def _authenticate(token: str) -> list[str]:
    with SessionLocal() as db:
        user = user_from_token(token, db)
        rows = db.query(Holding.symbol).filter(Holding.user_id == user.id).limit(MAX_SYMBOLS).all()
        return sorted({r.symbol for r in rows})


def _snapshot(symbols: list[str]) -> dict:
    return {s: get_quote(s).to_dict() for s in symbols}


@ws_router.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    await websocket.accept()
    try:
        first = await asyncio.wait_for(websocket.receive_json(), timeout=AUTH_TIMEOUT_SECONDS)
        if not isinstance(first, dict) or first.get("type") != "auth" or not first.get("token"):
            await websocket.close(code=POLICY_VIOLATION)
            return
        symbols = await run_in_threadpool(_authenticate, str(first["token"]))
    except (asyncio.TimeoutError, HTTPException, ValueError):
        await websocket.close(code=POLICY_VIOLATION)
        return
    except WebSocketDisconnect:
        return

    try:
        while True:
            data = await run_in_threadpool(_snapshot, symbols)  # provider calls are blocking
            await websocket.send_json({"type": "prices", "data": data, "ts": datetime.now(timezone.utc).isoformat()})
            await asyncio.sleep(INTERVAL_SECONDS)
    except WebSocketDisconnect:
        return
