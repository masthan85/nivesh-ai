from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.utils.security import SecurityHeadersMiddleware
from app.utils.request_context import RequestContextMiddleware, InMemoryRateLimitMiddleware
from app.database import SessionLocal

import app.models.user  # noqa: F401
import app.models.portfolio  # noqa: F401
import app.models.goal  # noqa: F401
import app.models.audit  # noqa: F401

if settings.AUTO_CREATE_SCHEMA and settings.ENVIRONMENT.lower() != 'production':
    Base.metadata.create_all(bind=engine)

from app.routers.auth import router as auth_router
from app.routers.portfolio import router as portfolio_router
from app.routers.market import router as market_router
from app.routers.broker import router as broker_router
from app.routers.tax import router as tax_router
from app.routers.goals import router as goals_router
from app.routers.watchlist import watchlist_router, alerts_router
from app.routers.ai_chat import router as ai_router
from app.routers.news import news_router
from app.routers.briefing import router as briefing_router
from app.routers.websocket import ws_router

app = FastAPI(
    title=f'{settings.APP_NAME} API',
    description='Investment intelligence platform. Financial outputs must disclose freshness and source limitations.',
    version=settings.API_VERSION,
    docs_url='/docs' if settings.ENVIRONMENT != 'production' else None,
    redoc_url='/redoc' if settings.ENVIRONMENT != 'production' else None,
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(InMemoryRateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['Authorization', 'Content-Type', 'X-Request-ID'],
)
for router in [auth_router, portfolio_router, market_router, broker_router, tax_router,
               goals_router, watchlist_router, alerts_router, ai_router, news_router,
               briefing_router, ws_router]:
    app.include_router(router)

@app.get('/', tags=['Health'])
def root():
    return {'service': settings.APP_NAME, 'version': settings.API_VERSION, 'status': 'running'}

@app.get('/health', tags=['Health'])
def health():
    return {'status': 'ok', 'service': settings.APP_NAME, 'timestamp': datetime.now(timezone.utc).isoformat()}

@app.get('/ready', tags=['Health'])
def ready():
    try:
        with SessionLocal() as db:
            db.execute(text('SELECT 1'))
        database = 'ready'
    except Exception:
        database = 'unavailable'
    ready_now = database == 'ready'
    body = {'status': 'ready' if ready_now else 'not_ready', 'database': database, 'market_data_mode': settings.MARKET_DATA_MODE}
    # Orchestrators read the status code, so an unready service must not answer 200.
    return JSONResponse(body, status_code=200 if ready_now else 503)
