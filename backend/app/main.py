"""
Nivesh AI — Backend Entry Point
FastAPI application with all routers registered.
Run: uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

# Import all models so SQLAlchemy creates tables
import app.models.user       # noqa
import app.models.portfolio  # noqa
import app.models.goal       # noqa

# Create all tables
Base.metadata.create_all(bind=engine)

# Import routers
from app.routers.auth      import router as auth_router
from app.routers.portfolio import router as portfolio_router
from app.routers.market    import router as market_router
from app.routers.broker    import router as broker_router
from app.routers.tax       import router as tax_router
from app.routers.goals     import router as goals_router
from app.routers.watchlist import watchlist_router, alerts_router
from app.routers.ai_chat   import router as ai_router
from app.routers.news      import news_router
from app.routers.briefing  import router as briefing_router
from app.routers.websocket import ws_router

app = FastAPI(
    title="Nivesh AI API",
    description="Nivesh AI — AI-powered investment intelligence built for India. Portfolio tracking, broker cost comparison, tax P&L, goal planning and AI advisor.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(market_router)
app.include_router(broker_router)
app.include_router(tax_router)
app.include_router(goals_router)
app.include_router(watchlist_router)
app.include_router(alerts_router)
app.include_router(ai_router)
app.include_router(news_router)
app.include_router(briefing_router)
app.include_router(ws_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Nivesh AI",
        "version": "2.0.0",
        "status":  "running",
        "docs":    "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    from datetime import datetime
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
