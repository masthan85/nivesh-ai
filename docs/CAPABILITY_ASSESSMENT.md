# Nivara AI capability assessment

Date: 30 September 2026. Scope: the `nivesh-ai-main` archive supplied on that date. This document supersedes the verification claims in `RELEASE_STATUS.md` and `PHASE-2-IMPLEMENTATION-REPORT.md` where they conflict.

## Summary

The repository is a compact backend prototype of roughly 1,300 lines of Python with a single-file React presentation shell. The backend foundations are better than the frontend suggests. Decimal arithmetic, NUMERIC columns, a clean Alembic baseline, a replaceable market-data provider with freshness metadata, and consistent per-user scoping on the core routes are real and now verified. As supplied, however, the API could not start with its pinned dependencies, the CI workflow would have failed on both backend tests and frontend lint, and the frontend is not connected to the backend at all. Several routes return hard-coded or advice-like content that contradicts the product's own principles.

Nivara is not production-ready, and it is not yet a usable end-to-end prototype, because no browser journey reaches real data.

## What was run in this assessment

Environment: Python 3.12.3 with the exact pinned `requirements.txt`, Node 22, PostgreSQL 16 installed locally. Docker was not available, so neither container image was built. The historical Docker build claims remain unverified.

| Check | Result |
|---|---|
| `pytest -q` as written in CI | Failed. No test could import `app` because nothing put `backend/` on the path |
| `import app.main` with pinned dependencies | Failed. pydantic 2.7.1 rejects `max_digits` on `Optional[Decimal]` fields, so the API cannot start |
| Existing 10 unit tests after the two fixes below | Passed |
| New API integration suite (10 tests) on SQLite and on PostgreSQL 16 | 7 passed, 3 confirmed defects (see below) |
| Alembic upgrade, `alembic check` drift test, downgrade, re-upgrade on PostgreSQL 16 | Passed. Models and migration agree; financial columns are `numeric(24,8)` and `numeric(24,4)` |
| Same migration on SQLite | Passed |
| `npm ci` and `npm run build` | Passed, 160 kB JS bundle |
| `npm run lint` as written in CI | Failed. No ESLint configuration existed |
| `npm run lint` after adding config and removing one unused import | Passed |
| `npm audit` | 4 advisories (1 high, 3 moderate), including esbuild dev-server and react-router |
| `pip-audit` on pinned backend requirements | Known advisories in starlette 0.37.2, python-multipart 0.0.9, python-jose 3.3.0, ecdsa and pytest |

Because the application could not import under its own pins, the earlier report of ten passing tests and a working stack must have come from a different environment or revision. Treat all pre-30-September verification as unconfirmed.

## Changes made during the assessment

Only changes needed to make verification possible, plus the tests themselves. Moving the schema constraints into `Annotated` types in `app/schemas/portfolio.py` restores startup without changing validation rules or version pins. A `backend/pytest.ini` sets the import path so the CI command works. `tests/conftest.py` and `tests/test_api_journeys.py` add isolated API-level tests, and the database can be switched to PostgreSQL through `TEST_DATABASE_URL`. `frontend/.eslintrc.cjs` adds a minimal configuration, and one unused React import was removed. The three confirmed defects are recorded as strict expected failures, so fixing one will force the marker's removal rather than leaving it silently stale.

## Capability status

**Authentication.** Registration, login, bcrypt hashing, JWT issue and rejection of bad or missing tokens all work at API level. Tokens identify users by email and cannot be revoked; a deactivated user's existing token continues to work until expiry (confirmed defect). There is no refresh flow, no logout, no brute-force control specific to login, and the rate limiter keys on client IP, which will collapse to a single key behind a reverse proxy. python-jose is effectively unmaintained and should be replaced with PyJWT.

**Authorisation.** Holdings and goals are correctly isolated between users for read, update and delete (verified). Watchlists and alerts use the same query pattern but are not yet covered by tests. The market, broker and WebSocket routes require no authentication. The `/ws/prices` stream accepts anonymous connections and makes blocking yfinance calls inside the async event loop.

**Portfolio.** Holdings CRUD works, duplicates are rejected, and valuation falls back to cost basis with an explicit disclosure flag when prices are unavailable (verified). The model holds a single average price and a free-text buy date per position. There are no transactions, lots, corporate actions or realised performance, so XIRR, accurate tax and import reconciliation are not possible on the current schema. Calculations use Decimal internally but convert to float in every API response.

**Market data.** The provider protocol and the explicit unavailable provider are sound. yfinance is correctly labelled development-only. Instrument search returns an empty list by design. There is no historical price, fundamentals or corporate-action capability.

**Briefing.** `/briefing/daily` returns hard-coded Nifty, Sensex and VIX values, a fixed "Bullish" market mood and four calendar events dated in May. It also generates directive text such as "Consider booking partial profits". This is fabricated data presented as fact alongside advice-like language, and it should be withdrawn before anyone outside the team sees it.

**News.** Pulled directly from yfinance with sentiment and impact fields hard-coded to neutral and medium. Not a licensed source and not portfolio-relevance ranked.

**Tax.** The rates appear to reflect post-July-2024 treatment of listed equity (20 percent short-term, 12.5 percent long-term above a ₹1.25 lakh exemption), subject to verification against current law. The calculator treats every unrealised holding as a trade, applies equity rules to every asset type including debt funds, ignores set-off of losses and pre-2018 grandfathering, and silently substitutes cost price when a quote is missing. It is a hypothetical illustration, correctly labelled as such in the response, but the README's "ITR-ready" claim must go.

**Broker costs.** Five illustrative rate cards, correctly labelled unverified in the response. An unknown broker ID produces a 500 error rather than a client error (confirmed defect). The README claims fifteen brokers.

**Goals and projections.** Deterministic SIP projections with fixed annual return assumptions by risk profile (8, 12 and 14 percent). There is no inflation treatment, no uncertainty range, and the assumed rate is not surfaced prominently enough for a user-facing projection.

**Watchlists and alerts.** Rules can be saved. Nothing evaluates or delivers them, so the product has alert rules, not alerts.

**Nia.** The backend route calls Anthropic with holdings, risk profile and SIP amount in the system prompt, degrades cleanly when unconfigured (verified), and persists messages. Conversation history is accepted from the client unvalidated, so a client can forge prior assistant turns or inject arbitrary roles (confirmed defect); history should come from the server's own store. The model identifier is hard-coded and should move to configuration. There is no retrieval, no tool use, no citation structure, no separation of fact types in the response, and no evaluation. The frontend Nia is a keyword-matched script and never calls the backend.

**Frontend.** A single `App.jsx` renders a navigation shell with demo holdings, a scripted Nia and placeholder pages. There is no router, no sign-in, and no use of the API client modules, which exist but are never imported. The README's page and component inventory describes files that do not exist.

**Operations.** Health and readiness endpoints exist, though `/ready` returns HTTP 200 even when not ready, which orchestrators will misread. The backend's `default-src 'none'` content security policy blocks the CDN scripts that Swagger's `/docs` page needs, so API docs will not render in a browser. There is no structured logging, metrics, backup or deployment path.

## Documentation and positioning

The README contradicts the product brief in ways that matter for a financial product: "Bloomberg Terminal + Zerodha + ChatGPT", "AI Financial Advisor", "Exact charges across 15 brokers", "ITR-ready", WhatsApp alerts, 72 connectors and a production compose file, none of which exist. It also declares an MIT licence without a LICENSE file. It should be rewritten to describe what exists.

## Recommended phase 2 order (as written before stabilisation)

First, fix the three confirmed defects, upgrade FastAPI/Starlette and python-multipart, replace python-jose, and make `/ready` return 503 when unready. Second, remove the fabricated briefing content and gate or authenticate the market and WebSocket routes. Third, rewrite the README. Fourth, and most important for the product, redesign the portfolio schema around transactions before building any import path, because every import, tax and performance feature depends on it. Only then connect the frontend journeys to the API.

## Stabilisation update, 30 September 2026

This section records the stabilisation pass completed after the assessment. It supersedes the defect and dependency findings above.

**Fixed.** Deactivated accounts now lose access immediately. An unknown broker returns 404 and invalid trade types return 422. Nia no longer accepts conversation history from the client; it reads history from its own store, takes its model from configuration (`ANTHROPIC_MODEL`) and sends only symbols, quantities and average cost to the model provider. `/ready` returns 503 when the database is unavailable. The API docs page has its own content security policy, so Swagger renders.

**Removed fabricated content.** The daily briefing no longer returns hard-coded index levels, market mood, calendar events or advice-style text. It reports only portfolio moves above 1.5 percent that the provider supports, with source and freshness, and states that market overview data is unavailable. News no longer reports invented sentiment or impact values.

**Tightened access.** Market routes require authentication and validate symbols. The price WebSocket authenticates through its first message, streams only the user's own holdings and runs provider calls off the event loop.

**Narrowed tax scope.** The tax illustration covers listed equity and equity ETFs only, excludes holdings without a quote instead of valuing them at cost, and lists what it does not cover.

**Dependencies.** FastAPI 0.142, Starlette 1.7, SQLAlchemy 2.1, pydantic 2.13 and python-multipart 0.0.32. python-jose and passlib are replaced by PyJWT and bcrypt, and passwords over bcrypt's 72-byte limit are rejected rather than silently truncated. Unused frontend packages (react-router-dom, recharts, zustand) are removed and Vite is upgraded to 8. `pip-audit` and `npm audit` both report no known vulnerabilities. The frontend image and CI move to Node 22; the backend image runs as a non-root user.

**Verified.** 26 backend tests pass on SQLite and on PostgreSQL 16, covering authentication, deactivation, ownership isolation across holdings, goals, watchlists and alerts, the briefing and tax scope rules, WebSocket authentication, and degraded providers. The Alembic migration round trip and drift check pass on PostgreSQL 16 with the upgraded SQLAlchemy. The API boots under uvicorn against PostgreSQL. Frontend lint and build pass. Docker images were not built in the assessment environment.

**Still open.** The frontend is not connected to the backend. The portfolio model has no transactions. Rate limiting is per-process and keyed on client IP. Tokens cannot be revoked except by deactivating the account. There is no structured logging, backup or deployment path.
