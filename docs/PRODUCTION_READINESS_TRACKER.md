# Nivara AI production-readiness tracker

Status reflects evidence in this repository as of 26 September 2026. “Verified” means a relevant automated or executable check was run in the current engineering environment. It does not imply external provider, regulatory or production infrastructure validation.

| Area | Status | Current evidence | Remaining release work |
|---|---|---|---|
| Application architecture | Implemented and verified | Modular FastAPI backend and React application shell compile/source reviewed | Continue separating domain services from route orchestration |
| PostgreSQL architecture | Implemented but awaiting infrastructure | PostgreSQL Docker service, psycopg driver, SQLAlchemy URL support | Run staging load and backup/restore tests |
| Alembic migrations | Implemented and verified | Clean SQLite migration test reaches revision `20260926_01` | Rehearse against staging PostgreSQL and define prototype-data migration procedure |
| Financial precision | Implemented and verified for core paths | NUMERIC persistence plus Decimal portfolio, broker, tax and goal calculations; automated precision tests | Extend Decimal discipline to every future monetary service; independently validate tax/broker rules |
| Market data abstraction | Partially implemented | Provider protocol, explicit unavailable provider, development yfinance adapter, source/freshness metadata | Select licensed production provider and implement/search/fundamental/corporate-action adapters |
| Authentication | Partially implemented | Password hashing, JWT access token, user scoping, active-user concept | Refresh/revocation strategy, MFA decision, cookie/session hardening, credential-stuffing controls |
| Authorization | Partially implemented | Portfolio/goals/watchlist queries are scoped by authenticated user | Add systematic authorization tests and policy layer for future shared/administrative capabilities |
| Rate limiting | Partially implemented | In-process development limiter | Replace with shared gateway/Redis limiter in production and tune per endpoint/user |
| Audit logging | Partially implemented | Persistent audit event model and login/register events | Cover financial mutations, security events, AI/tool actions; retention and integrity controls |
| Nia AI | Partially implemented | Portfolio-context-only prompt, explicit provider failure, no fabricated confidence score | Grounded retrieval, citations, tool authorization, prompt-injection controls, model abstraction, evals, telemetry |
| Frontend | Partially implemented | Responsive shell with Home, Markets, Research, Portfolio, Watch, Nia | Full authenticated journeys plus Risk, Goals, Tax, Broker Costs, What-if, News, Alerts, Connections, Settings |
| Observability | Partially implemented | Request IDs, Server-Timing, health/readiness | Structured logs, metrics, traces, provider health, AI token/cost telemetry, SLOs/alerts |
| CI/CD | Partially implemented | Compile, tests, migration check, frontend lint/build, dependency and secret scanning configured | Execute in connected CI, add container scan, staging deployment, smoke test and rollback proof |
| Security | Partially implemented | CORS allowlist, security headers, production secret checks, validation | ASVS verification, threat model, CSRF/session design, DAST, dependency remediation, penetration testing |
| Backups/recovery | Not implemented | None | PostgreSQL backup policy, encryption, retention, restore drill and RPO/RTO evidence |
| Data licensing | Blocked | Development provider intentionally marked non-production | Commercial/licensing decision required before live launch |
| Production deployment | Blocked | Local Docker architecture only | Cloud environment, secrets manager, TLS/domain, staging/prod separation, health/rollback verification |

## Release decision

Nivara AI remains **not production-ready**. The foundation now has materially stronger persistence, financial precision, provider isolation and engineering gates, but launch remains blocked by licensed financial-data sources, full authentication/session hardening, current India tax/broker-rule validation, observability, end-to-end testing, security verification, backups and a rehearsed production deployment.
