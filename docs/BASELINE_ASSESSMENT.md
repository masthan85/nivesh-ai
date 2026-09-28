# Nivara AI baseline assessment

## Executive summary

The repository is a useful backend prototype, not yet a production application. FastAPI routes exist for authentication, portfolio, markets, broker costs, tax, goals, watchlists, news, briefing, AI chat and WebSockets. The checked-in frontend, however, originally contained only API helper modules; the README described a much larger React application that was not present in the archive. This build adds a real React application shell so the repository can be built and visually evaluated.

## Working foundations

Authentication uses hashed passwords and signed JWT bearer tokens. User ownership filters are present on holdings and most user-specific records. Portfolio, goal, tax and broker calculation logic exists. Market data is isolated in a service module. Docker definitions exist for backend and frontend.

## Partial or unsafe areas found

The application previously enabled wildcard CORS together with credentials. A development JWT secret had an insecure default. New registrations silently received fabricated holdings and goals. The AI prompt requested unsupported confidence scores and did not safely handle provider errors. Financial values use binary floating point throughout. Market data is obtained from yfinance without a production licensing decision, freshness contract or provider abstraction. There is no migration workflow in use despite Alembic being listed. No checked-in tests, CI pipeline, production compose override, reverse-proxy directory, observability stack or release runbook were present in the supplied archive. The README overstated the actual repository contents.

## Current remediation in this build

The product-facing shell is renamed Nivara AI. CORS is allowlisted, production secret validation is enforced, demo seeding is opt-in, request schemas have tighter validation, basic security headers are added, Nia provider failures now degrade explicitly, fabricated AI confidence scores are removed, and a minimal verification suite is added. The frontend now contains a responsive application shell with Home, Markets, Research, Portfolio, Watch and Nia workspaces and clear demo-data labelling.

## Still required before production

PostgreSQL plus Alembic migrations, precision-safe money types, an external market-data provider with licensed production rights, news and fundamentals providers, server-side rate limiting, secure session/token strategy review, refresh/revocation, MFA decision, audit logging, provider adapters, job processing, Redis or equivalent cache, observability, tracing, SLOs, backups, CI/CD security gates, dependency and secret scanning, accessibility testing, comprehensive financial tests, end-to-end tests, broker and tax rule verification, data-retention/privacy controls, and a formal threat model remain outstanding.
