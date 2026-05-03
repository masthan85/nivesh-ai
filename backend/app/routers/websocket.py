"""routers/websocket.py — Live price streaming"""
import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.market_data import get_live_price

ws_router = APIRouter(tags=["WebSocket"])

STREAM_SYMBOLS = ["RELIANCE", "INFY", "HDFCBANK", "WIPRO", "TCS", "TATAMOTORS", "NIFTY50"]


@ws_router.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            prices = {}
            for sym in STREAM_SYMBOLS:
                ltp, chg = get_live_price(sym)
                prices[sym] = {"ltp": ltp, "change_pct": chg}
            await websocket.send_json({
                "type": "prices",
                "data": prices,
                "ts":   datetime.utcnow().isoformat()
            })
            await asyncio.sleep(15)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
