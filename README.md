# Nivara AI

Nivara AI is an early-stage investment-understanding workspace for Indian retail investors, previously developed as Nivesh AI. It aims to bring a user's holdings, research and planning together with Nia, a research assistant that explains rather than advises.

This repository is a working prototype. It is not production-ready, and several capabilities described in the product vision are not built yet. `docs/CAPABILITY_ASSESSMENT.md` records exactly what exists and what has been verified.

## What works today

The FastAPI backend supports registration and sign-in, per-user holdings, goals, watchlists and saved alert rules, with ownership isolation covered by automated tests. Portfolio valuation, goal projections, tax illustrations and broker-cost illustrations are deterministic Decimal-based services. PostgreSQL is the system of record, with Alembic migrations.

Market data sits behind a replaceable provider interface. The only adapter is a development adapter using yfinance, which is not a licensed source and is never labelled as live. Every quote carries its source, timestamp and freshness, and missing prices are reported as unavailable rather than invented.

Nia's backend route answers using only the user's own holdings as context. It has no live market data, news, retrieval or tools yet, and it says so.

The React frontend is currently a presentation shell with clearly labelled demo data. It is not yet connected to the backend.

## What is illustrative or not built

Tax output is a hypothetical illustration for listed equity, not a filing-ready computation. Broker rate cards cover five brokers and are unverified. Alert rules are saved but not evaluated or delivered. There are no broker or depository connections, no licensed market, fundamentals or news data, and no notification services.

## Running locally with Docker

You need Docker Desktop.

```bash
cp backend/.env.example backend/.env
# Set SECRET_KEY to a random value of at least 32 characters.
# ANTHROPIC_API_KEY is optional; without it Nia reports that it is not configured.
docker compose up --build
```

The frontend is served on http://localhost:3000 and the API on http://localhost:8000, with interactive API docs at http://localhost:8000/docs and readiness at http://localhost:8000/ready. Database migrations run automatically when the backend container starts.

## Running without Docker

The backend needs Python 3.11 or later and a database. SQLite works for quick local use.

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

The frontend needs Node 22 LTS (or Node 20.19 or later).

```bash
cd frontend
npm ci
npm run dev
```

## Tests

```bash
cd backend
pytest -q
TEST_DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/nivara pytest -q   # against PostgreSQL
```

CI runs the backend suite on SQLite and PostgreSQL, a migration round trip with drift detection, frontend lint and build, dependency audits and secret scanning.

## Important notice

Nivara AI provides information and illustrations for educational purposes. It is not investment advice, and Nivara AI is not registered with SEBI as an investment adviser or research analyst. The regulatory position of planned features has not yet been reviewed by qualified advisers.

## Licence

No licence has been chosen yet. Until one is added, all rights are reserved by the author.
