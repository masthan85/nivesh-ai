# Nivara AI release status

## Implemented and verified

Core financial persistence now uses SQL `NUMERIC` for portfolio quantities, average prices, goals, watch targets, alert prices and monthly investment amounts. Portfolio valuation, broker-cost calculations, tax summaries and goal projections use Decimal-based domain calculations. Ten backend tests pass, including precision edge cases, annual LTCG exemption behaviour and the rule that an unavailable market provider never fabricates a price.

A clean Alembic migration was executed successfully against an empty database and reached revision `20260926_01`. The migration creates the core user, holding, goal, watchlist, alert, chat and audit tables.

Market data now sits behind a provider contract. The existing yfinance source is explicitly a development-only adapter. Quote responses carry source, timestamp, freshness and live/non-live state. When no provider can return a price, the system returns unavailable status rather than inventing a value.

Request correlation and a development rate limiter are present. Authentication registration/login now records audit events. PostgreSQL development composition, migration-first startup and initial CI security gates are configured.

## Implemented but awaiting connected infrastructure

The Docker development stack is configured for PostgreSQL, but PostgreSQL containers were not started in the current runtime. The CI workflow now includes backend tests, migration validation, dependency scanning, frontend lint/build/audit and secret scanning; it still needs execution in GitHub Actions.

## Partially implemented

Authentication still uses bearer access tokens stored by the current frontend and does not yet provide refresh/revocation, MFA or a fully hardened browser-session design. The rate limiter is process-local and must be replaced by a shared production control. Audit coverage currently focuses on authentication rather than all financial and AI mutations.

Nia remains portfolio-context-only. It does not yet have grounded external retrieval, source citations, provider abstraction, authorised tool execution, evaluation datasets or model-cost telemetry.

The frontend shell exists but most workspaces still require full production journeys and API integration.

## Blocked or requiring decisions

A licensed production provider for Indian market prices, fundamentals, corporate actions and news has not been selected. Tax and broker rules are intentionally labelled illustrative until independently validated against current authoritative sources. Production cloud accounts, secrets infrastructure, notification services, domain/TLS, backups and rollback infrastructure are not configured.

## Verification limitations in this environment

Backend source compilation succeeds. The backend test suite passes with 10 tests. Alembic clean-database migration verification succeeds. Full FastAPI authentication integration testing is blocked because `python-jose` and `passlib` are not installed in this runtime. Frontend dependency installation timed out, so the Vite production build and ESLint run could not be executed here.

## Release decision

Not production-ready. See `PRODUCTION_READINESS_TRACKER.md` for the evidence-based status by capability.
