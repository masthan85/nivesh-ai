# Nivara AI (formerly Nivesh AI): codebase audit, vision vs. built state vs. gaps

Audit date: 25 November 2026. Repository: /home/user/nivesh-ai, HEAD `10571fa` ("updating the front end files", 2026-10-06). Seven commits, 2026-09-28 to 2026-10-06 (`git log`). Read-only audit: no repository files were modified (`git status --short` was empty before and after). Citations of the form `path:line` refer to files in the repository. Commands were run in this session on Python 3.13.18 and Node 22.23.5 / npm 10.9.9.

## 1. Product vision, target user, requirements, and claimed capability status

### Takeaway
The product is pitched as an "investment-understanding workspace for Indian retail investors". It pulls holdings, research and planning together with "Nia", an AI research assistant that "explains rather than advises". The docs are now unusually candid. They describe a backend prototype with Decimal-based calculators and a frontend shell. Most of the vision is unbuilt: licensed data, transactions, alerts delivery, Nia retrieval and tools, and most UI journeys.

### Cited Findings
- Vision and target user: "early-stage investment-understanding workspace for Indian retail investors … with Nia, a research assistant that explains rather than advises". The README also says the repository "is a working prototype. It is not production-ready" — README.md:3-5
- Regulatory posture: the product is "not investment advice", Nivara "is not registered with SEBI as an investment adviser or research analyst", and the regulatory position "has not yet been reviewed" — README.md:71-73. No licence has been chosen — README.md:77
- Target architecture: a modular monolith. The React client talks to a "versioned FastAPI application". Domain modules cover portfolio, goals, taxes, broker costs, risk and alerts. Providers sit behind adapters. PostgreSQL is the system of record, Redis is "reserved" for caching, and async workers handle alerts, imports and briefings. LLMs must never do financial calculations. Nia "orchestrates retrieval and approved tools". Every datum carries source, timestamp, timezone and freshness — docs/ARCHITECTURE.md:3-5; ADR-001 (docs/ADR-001-MODULAR-MONOLITH.md:5)
- ADR-002 says to use Decimal/NUMERIC everywhere, with float "only at presentation boundaries" — docs/ADR-002-FINANCIAL-PRECISION.md:5,13. ADR-003 requires replaceable market-data providers. yfinance is a development-only adapter, and missing data must be reported as unavailable, never fabricated — docs/ADR-003-MARKET-DATA-PROVIDERS.md:5-11
- Security model: verify against OWASP ASVS 5.0 and OWASP AISVS. Tools must be allowlisted and re-authorised on the server. Retrieved text is untrusted — docs/SECURITY_MODEL.md:3-7
- Testing strategy: financial-correctness fixture tests with authoritative reference examples, API integration tests, browser E2E tests, and AI prompt-injection tests — docs/TESTING_STRATEGY.md:3-7
- Claimed as built (README "What works today"): registration and sign-in, per-user holdings, goals, watchlists and saved alert rules with ownership isolation, Decimal valuation/goal/tax/broker-cost services, PostgreSQL plus Alembic, a provider interface with a yfinance dev adapter, and Nia answering from holdings only — README.md:9-15
- Claimed as illustrative or not built: tax output is "hypothetical", broker rate cards are "five brokers and are unverified", alert rules are "saved but not evaluated or delivered", and there are no broker/depository connections, licensed data or notifications — README.md:19-21. This last line is contradicted by the README's own later "Broker connections" section (README.md:79-87).
- Production-readiness tracker (dated 26 Sep 2026) statuses:
  - Implemented and verified: architecture, migrations, financial precision.
  - Partially implemented: market data, authentication, authorisation, rate limiting, audit logging, Nia, frontend, observability, CI/CD, security.
  - Not implemented: backups.
  - Blocked: data licensing, production deployment.
  - Release decision: "not production-ready" — docs/PRODUCTION_READINESS_TRACKER.md:5-27
- CAPABILITY_ASSESSMENT.md (30 Sep 2026) supersedes RELEASE_STATUS.md and PHASE-2-IMPLEMENTATION-REPORT.md "where they conflict" — docs/CAPABILITY_ASSESSMENT.md:3; docs/RELEASE_STATUS.md:3. It found that the code as supplied could not even start under its pins (pydantic `max_digits` on Optional[Decimal]), that CI would have failed, and that pre-30-September verification is "unconfirmed" — docs/CAPABILITY_ASSESSMENT.md:7-29
- Its "Stabilisation update" claims these fixes:
  - Deactivated users are rejected.
  - Unknown broker returns 404.
  - Nia history is server-side, and the model comes from config.
  - `/ready` returns 503.
  - The fabricated briefing is removed.
  - Market and WebSocket routes are authenticated.
  - Tax scope is narrowed.
  - python-jose and passlib are replaced by PyJWT and bcrypt.
  - pip-audit and npm audit were clean.
  - "26 backend tests pass". "Frontend lint and build pass."
  - Still open: frontend not connected, no transactions, per-process IP rate limit, no token revocation, no logging, backup or deployment.
  - docs/CAPABILITY_ASSESSMENT.md:71-87
- PHASE-2 report (26 Sep) claims "10 backend tests passed" and that frontend lint/build "could not be executed" — docs/PHASE-2-IMPLEMENTATION-REPORT.md:17. BASELINE_ASSESSMENT lists the original defects: wildcard CORS with credentials, an insecure JWT default, fabricated seeded holdings, AI confidence scores, and floats throughout — docs/BASELINE_ASSESSMENT.md:13
- Broker vision: never collect broker passwords, read-only first, tokens are secrets and never logged, Groww tokens are not persisted, and broker data is not merged into the canonical portfolio until reconciliation exists — docs/BROKER_CONNECTIONS.md:5-11. Production follow-up requires an encrypted connection store with KMS, revocation, consent history and rotation — docs/BROKER_CONNECTIONS.md:52

### Inferences
- The requirement set is implicit, spread across ARCHITECTURE, SECURITY_MODEL, TESTING_STRATEGY and the tracker's "remaining release work" column. There is no PRD, user-story list or acceptance criteria in the repository.
- The workspaces named in the tracker (Risk, Goals, Tax, Broker Costs, What-if, News, Alerts, Connections, Settings — docs/PRODUCTION_READINESS_TRACKER.md:18) describe the product scope. Of these, only Connections exists as UI.

### Gaps
- No user research, persona detail, pricing/business model or regulatory analysis (SEBI IA/RA, the Account Aggregator framework) appears anywhere in the repository.
- The tracker is dated 26 Sep 2026 and has not been updated since the stabilisation pass or the broker-connection commit. Its status column is stale.

## 2. Where code and docs diverge

### Takeaway
The README's line "not yet connected to the backend" is now partly false. Since commit 10571fa the frontend imports `authAPI` and `brokerAPI` and runs real sign-in, registration and Groww snapshot calls. Portfolio, Home, Nia and Markets remain hard-coded demo content, and four of the five `src/api/*.js` modules are still unused. Several documented "verified" claims also no longer hold: lint fails and npm audit is not clean.

### Cited Findings
- README says "The React frontend is currently a presentation shell with clearly labelled demo data. It is not yet connected to the backend" — README.md:17. CAPABILITY_ASSESSMENT says the API client modules "exist but are never imported" — docs/CAPABILITY_ASSESSMENT.md:63.
- Actual state:
  - `App.jsx` imports `authAPI` and `brokerAPI` — frontend/src/App.jsx:3-4.
  - On load it calls `brokerAPI.providers()` and `authAPI.me()` — frontend/src/App.jsx:47-53.
  - Login and register use the real API and store the JWT — frontend/src/App.jsx:76-99.
  - The Groww preview and Motilal login are real calls — frontend/src/App.jsx:118-155.
  - The README's later "Broker connections" section acknowledges this — README.md:79-87.
  - So the README contradicts itself (line 17 vs. lines 79-87, and line 21 "no broker … connections").
- Still demo or unwired:
  - `demoHoldings` are hard-coded — frontend/src/App.jsx:11-16.
  - Nia is keyword-matched and never calls `/ai/chat` — frontend/src/App.jsx:64-73.
  - `api/portfolio.js` and `api/market.js` are not imported anywhere (only `auth` and `brokers` are imported, App.jsx:3-4).
  - Markets, Research and Watch render a generic "FOUNDATION BUILD" placeholder (`renderGeneric`, App.jsx ~line 244).
- Client and API contract drift:
  - `getTaxSummary(fy)` sends `?fy=` — frontend/src/api/portfolio.js:10. The backend `/tax/summary` takes no `fy` parameter — backend/app/routers/tax.py:22-23.
  - `marketAPI.getPrices` builds a query string by string concatenation without encoding — frontend/src/api/market.js:5.
- The "Account" page is reachable only by redirect (`setActive('Account')`, App.jsx:58,114,142). It is not in the `nav` array — App.jsx:5-8.
- Lint: CAPABILITY_ASSESSMENT says "Frontend lint and build pass" (docs/CAPABILITY_ASSESSMENT.md:85). In this session `npm run lint` failed with 2 errors (`react/no-unescaped-entities` at App.jsx:212:42 and 215:94). These lines came in with the 6 Oct broker commit, so CI's `npm run lint` step (.github/workflows/ci.yml:68) would fail on HEAD.
- npm audit: the docs say it was clean (docs/CAPABILITY_ASSESSMENT.md:81). In this session `npm audit --audit-level=high` exited 1 with "3 high severity vulnerabilities": vite (GHSA-9jrq-w75r-8gcw, GHSA-rq7h-c2jc-7f22, GHSA-vfpm-58rq-9qcg) and launch-editor (GHSA-r825-w8mm-5pxw and others). CI step .github/workflows/ci.yml:70 would therefore also fail. These are dev-server advisories published after 30 Sep, and none affects the nginx production bundle.
- Test count: the docs say 26 tests (docs/CAPABILITY_ASSESSMENT.md:85). There are now 30, adding 4 broker-connection tests (backend/tests/test_api_journeys.py:155-201). No `xfail` markers remain: `grep xfail` found nothing, although the assessment describes "strict expected failures" (line 33).
- Caching: ARCHITECTURE reserves Redis for caching (docs/ARCHITECTURE.md:3). `backend/app/utils/cache.py` defines `get_cached_price`/`set_cached_price` (lines 9-18), but nothing imports them (grep across app/ and tests/). It is dead code, and every quote is fetched live from yfinance on every request.
- The legacy `get_live_price` wrapper (backend/app/services/market_data.py:22-29) is also unused, and it returns `0.0` prices when data is unavailable. That would contradict ADR-003 if anything used it.
- ADR-002 says float only at boundaries, and the code does convert at the boundary. But `as_number` returns `float` for every API response (backend/app/domain/money.py:24-26). `goals.py` compares the float `projected` against a Decimal `target` and computes `gap` in floats (backend/app/routers/goals.py:19,33-34). Decimal precision is lost at the JSON edge, so clients receive binary floats for money.
- The ARCHITECTURE doc's "versioned FastAPI application" is not implemented. Routes have no `/v1` prefix (backend/app/main.py:49-52). `API_VERSION` exists only as metadata (backend/app/config.py:10).
- MIGRATIONS.md mentions "a prototype SQLite database" in the repository (docs/MIGRATIONS.md:5). No `.db` file is tracked in the file listing.

### Inferences
- The documentation is a better guide to intent than to state. At least three verification claims (lint passes, audits clean, 26 tests) are stale relative to HEAD. The last commit (frontend + broker) evidently did not go through the CI it describes.
- The frontend has only one real end-to-end journey: sign in → Connections → Groww snapshot. No browser journey reaches the Nivara portfolio, tax, goals or Nia APIs.

### Gaps
- Whether GitHub Actions has actually run on this repository could not be checked. No remote or run history was inspected; `gh` was not used.
- Docker images were not built in this session, so the README's Docker instructions remain unverified, as the assessment also says.

## 3. Correctness, security and reliability defects

### Takeaway
The previous assessment fixed the most glaring problems, and authorisation scoping on CRUD routes is consistently correct. Real defects remain:
- An email-case login bug, verified here.
- A production secret check that accepts the publicly known `.env.example` value, verified here.
- The JWT kept in localStorage with no CSP on the SPA.
- An IP-keyed, unbounded, per-process rate limiter.
- An unbounded `X-Request-ID` written into a `String(64)` audit column.
- Blocking, uncached yfinance calls inside request handlers.
- Tax calculations without loss set-off or the 4% cess.
- Out-of-date statutory charge rates: F&O STT, NSE transaction charges, and side-of-trade handling.

### Cited Findings

**Authentication and JWT**
- **[Verified defect] Email case.** Registering `Mixed@Example.COM` stores `Mixed@example.com`, because pydantic `EmailStr` normalises only the domain (backend/app/schemas/user.py:23). Login looks up the raw `form.username` (backend/app/routers/auth.py:42). Probe results: login with the exact typed address returned 401, login with the fully lowercased address returned 401, and only the exact normalised form returned 200. Registering `mixed@example.com` afterwards succeeded (200), creating a case-variant duplicate account. The register lookup is also case-sensitive (auth.py:22).
- **[Verified defect] Production secret check.** The check rejects only a key shorter than 32 characters or the literal 'change-this-in-production' (backend/app/config.py:43). The `.env.example` value `change-this-to-a-random-secret-key-min-32-chars` (backend/.env.example:2) is 47 characters long. `Settings(ENVIRONMENT=production, SECRET_KEY=<that value>)` validated without error in this session. Anyone who copies the template and forgets to change it gets a publicly known HS256 signing key, and with it full token forgery.
- The default dev `SECRET_KEY` (config.py:11) is 25 characters. That is below PyJWT's HS256 minimum key-length recommendation; a PyJWT key-length warning was emitted during the probe.
- JWTs carry only `sub`=email, `iat` and `exp`: no `jti`, `aud`, `iss` or token type (backend/app/utils/auth.py:31-34). There is no refresh, logout or revocation, apart from deactivation, which is now checked per request (auth.py:56-59). The lifetime may be up to 1440 minutes (config.py:29).
- There is no login-specific brute-force control or lockout. Failed logins are audited with the submitted email (auth.py:44-47), but nothing reads the audit table.
- Registration is an email-existence oracle: it returns 409 "Email already registered" (auth.py:22-23).

**Token storage and CORS**
- The JWT is stored in `localStorage['nivara_token']` and attached as a Bearer header (frontend/src/api/client.js:12-13; App.jsx:90). Any XSS exposes it. The nginx config sets no Content-Security-Policy or HSTS (frontend/nginx.conf:6-8). The backend CSP (backend/app/utils/security.py:4) protects only JSON responses, not the SPA.
- CORS is an explicit allowlist with `allow_credentials=True` (backend/app/main.py:42-48). Credentials are unnecessary, because auth is a bearer header rather than a cookie. The wildcard is blocked only in production (config.py:45-46).
- The middleware order puts CORS outermost, so 429 responses still carry CORS headers. That ordering is correct.

**Rate limiting**
- `InMemoryRateLimitMiddleware` keys on `request.client.host` (backend/app/utils/request_context.py:33). Behind nginx or a load balancer, every user collapses to one key; no `X-Forwarded-For`/ProxyHeaders handling is configured.
- `_hits` is a `defaultdict(deque)` that is never pruned of idle keys (request_context.py:27,36). Memory grows with the number of distinct IPs.
- The limit is per process and global (120/min), not per endpoint, so login and Groww preview get no tighter limits.
- The limiter takes a `threading.Lock` inside an async dispatch (request_context.py:35), which is minor but blocks the loop. The WebSocket route bypasses the `BaseHTTPMiddleware` limiter, which applies to HTTP only.

**Request ID and audit logging**
- `X-Request-ID` is taken verbatim from the client, with no length or charset check, and echoed back (request_context.py:13,17). The probe echoed a 5,000-character value.
- The same value is written to `audit_events.request_id String(64)` (backend/app/models/audit.py:13) on register, login and Groww connect. On PostgreSQL a long header would make the audit insert fail with "value too long", turning login into a 500. This was not executed on PostgreSQL; it is inferred from column types.
- Audit coverage is limited to `auth.register`, `auth.login` and `broker.groww.connect` (auth.py:34,45,49,52; broker.py:43-63). These are not audited: profile updates (auth.py:62-68), holding, goal, watchlist and alert mutations, Nia calls, and Motilal URL generation.
- There is no tamper-evidence, retention policy or read path. `audit_events.user_id` is a foreign key without `ondelete` (audit.py:10), so user deletion is not designed.
- The failure-reason string from Groww is stored in audit metadata (broker.py:50). It is safe today because the messages are fixed strings (backend/app/services/broker_connections.py:73-93).

**Broker tokens: Groww**
- The token travels in a JSON body and is not persisted or logged by the app (broker.py:41; broker_connections.py:82-93), which matches the docs.
- `httpx.Client(follow_redirects=False)` with a 12 s timeout is good practice (broker_connections.py:89).
- Defects:
  - `_payload` calls `body.get` without checking that `body` is a dict. A JSON array or `null` response raises `AttributeError` and returns a 500 instead of `BrokerConnectionError` (broker_connections.py:70-79).
  - JSON parsing happens before the status check, so a non-JSON 401 or 5xx is reported as "unreadable" rather than "rejected" (lines 70-75).
  - Any authenticated Nivara user can use the endpoint as an oracle to validate arbitrary Groww tokens, with only the global IP rate limit as protection.
  - The response returns the broker UCC and vendor user id (lines 122-129), and the UI displays the UCC (App.jsx ~line 205).
  - The snapshot is kept only in React state, so a page refresh loses it.

**Broker tokens: Motilal Oswal**
- `motilal_login_url()` puts `MOTILAL_API_KEY` into the URL returned to the browser (broker_connections.py:54-58; broker.py:67-81). The `.env` comment treats it as a secret (backend/.env.example:15-16).
- There is no `state`/nonce parameter for CSRF and login binding, and no callback route. The docs acknowledge that callback handling is missing (docs/BROKER_CONNECTIONS.md:40).
- The API key is not URL-encoded.
- `/broker/providers` and `/broker/calculate` are unauthenticated (broker.py:23-26,84-86; probe returned 200 for both). That is harmless for static data, but inconsistent with the "not an open proxy" stance in market.py:1.

**AI chat route**
- Positive points:
  - History comes from the server store (backend/app/routers/ai_chat.py:45-57).
  - Client history is rejected with `extra='forbid'` (backend/app/schemas/portfolio.py:75-80).
  - The model is configurable (config.py:13).
  - Errors map to 503, 504 and 502 (ai_chat.py:62-83).
  - Messages are persisted only after success (lines 85-87).
- Prompt-injection risk: holding `symbol` is regex-constrained, but the system prompt interpolates `h.symbol`, `h.qty` and `h.avg_price` plus `user.risk`/`user.horizon` (ai_chat.py:26-32). The `name` and `notes` fields are not sent. Injection surface in the system prompt is therefore low. The free-text `message` itself is user content, which is acceptable.
- Rule 7 (ai_chat.py:41) is a prompt-level control only. There is no output filtering for advice-like language, despite rule 5.
- Reliability issues:
  - The `httpx.AsyncClient` is created per request (ai_chat.py:68).
  - The handler does synchronous SQLAlchemy queries inside an `async def` (lines 65-66, 85-87, and `_server_history`), which blocks the event loop on every chat.
  - `resp.json()` is outside the try block, so non-JSON provider output gives a 500 (line 80).
  - The `anthropic-version: 2023-06-01` header is hard-coded (line 71).
  - The default model id `claude-sonnet-5-5` is hard-coded in config (config.py:13; backend/.env.example:9).
  - There are no per-user token or cost limits, and no telemetry.
  - `/ai/history` returns all stored messages, with no deletion or retention control (ai_chat.py:97-107).
  - Persisted history only keeps the role alternation correct if every turn succeeded. A user turn stored without its assistant reply cannot happen today, because both are saved together.
  - `max_tokens` is fixed at 1000 (line 72).

**WebSocket**
- Authentication via the first message, a 10 s timeout, scoping to own holdings, at most 25 symbols, and provider calls in the threadpool are all sound (backend/app/routers/websocket.py:20-57).
- Gaps:
  - The token is checked once, so a deactivated user or an expired token keeps streaming indefinitely (lines 45-56).
  - The holdings list is frozen at connect time.
  - There is no limit on concurrent connections per user or IP.
  - There is no Origin check (no CSWSH protection, mitigated by token-in-message).
  - `json.JSONDecodeError` from non-JSON first frames is a `ValueError`, so it is handled (line 46).
  - Each loop iteration makes up to 3 × 25 sequential yfinance calls.

**Market data and caching**
- `YFinanceDevelopmentProvider.get_quote` tries `.NS`, `.BO` and bare symbol in sequence, with blind `except Exception` (backend/app/providers/yfinance_provider.py:14-32).
- It ignores the holding's stored `exchange`, so BSE holdings are priced from NSE first.
- `as_of` is the fetch time, not the exchange timestamp (line 25). That overstates freshness against the ADR-003 requirement for a market timestamp (docs/ARCHITECTURE.md:5 asks for "market timezone").
- No caching is in effect (cache.py is unused). `/portfolio/holdings`, `/portfolio/summary`, `/tax/summary`, `/briefing/daily` and `/watchlist/` each make N blocking network calls per request in sync handlers (portfolio.py:26-27,62-63; tax.py:30; briefing.py:31-32; watchlist.py:19-20). Latency and threadpool exhaustion follow, since FastAPI's default is about 40 threads.

**Tax calculator (Indian rules)**
- Rates: STCG 20%, LTCG 12.5%, ₹1.25 lakh LTCG exemption (backend/app/services/tax_calculator.py:8-10). These match Budget July 2024 (effective 23 Jul 2024) for listed equity: "LTCG … 12.5% above a ₹1.25 lakh annual exemption … STCG … 20%" — [Business Standard](https://www.business-standard.com/markets/news/budget-2024-hikes-ltcg-tax-rate-to-12-5-stcg-to-20-stt-on-f-o-also-up-124072300553_1.html); [Bajaj Finserv](https://www.bajajfinserv.in/investments/section-112a-income-tax-act). That source says Section 112A of the 1961 Act is succeeded by Section 198 of the Income-tax Act, 2025, effective 1 April 2026. The code and docs reference neither Act.
- **[Verified defect] No loss set-off.** `stcg_tax = max(0, stcg) * 20%` ignores STCL, and `ltcg_taxable` ignores LTCL and STCL (tax_calculator.py:56-60). Probe: +₹1,00,000 STCG and −₹1,00,000 STCL produced `total_tax 20000.0`, when the net short-term gain is zero. The route lists set-off as "not covered" (backend/app/routers/tax.py:43), but the headline `total_tax` is still materially overstated.
- No 4% Health and Education Cess and no surcharge are applied (tax_calculator.py:58-60). Worked examples apply 4% cess on top of 12.5% LTCG — [TaxGuru](https://taxguru.in/?p=1052279). So `total_tax` is understated whenever gains are net positive. The route's "not_covered" list (tax.py:42-47) does not mention this.
- A missing or unparsable `buy_date` silently defaults to 400 days, which classifies the holding as LTCG (tax_calculator.py:33-36; probe confirmed `days: 400, type: LTCG` for an empty date). This is a silent assumption that favours the lower rate.
- `buy_date` is free text with no date validation (backend/app/schemas/portfolio.py:22; backend/app/models/portfolio.py:19).
- Holding-period test: `days > 365` (tax_calculator.py:11,18) approximates "more than 12 months". "Now" is taken in UTC, not IST (line 25).
- `asset_type == 'ETF'` is treated as equity (tax.py:19). Gold, debt and international ETFs are not equity-oriented, so the rates would be wrong for them.
- The per-trade `indicative_tax` is computed only for STCG; it is always 0 for LTCG (tax_calculator.py:44).
- `getcontext().prec = 34` mutates the global Decimal context at import time (tax_calculator.py:6).
- Goal projections live in `tax_calculator.py` (lines 78-110). They use fixed 8/12/14% returns with no inflation adjustment or uncertainty range, and the docs flag the same issue (docs/CAPABILITY_ASSESSMENT.md:55).

**Broker charges (statutory)**
- F&O STT is outdated and not split. The code uses a single `fo` rate of 0.0005 (0.05%) applied to notional (backend/app/services/broker_charges.py:34). Since Budget 2026-27, effective 1 April 2026, futures STT is 0.05% on the sell side, up from 0.02%, and options STT is 0.15% of the premium on the sell side, up from 0.10% — [Business Standard](https://www.business-standard.com/markets/news/markets-fm-hikes-stt-on-fo-trades-surprise-move-126020100888_1.html); [Business Today](https://www.businesstoday.in/markets/story/stt-hike-on-fo-trades-to-take-effect-from-april-1-trading-costs-to-rise-522428-2026-03-26); [ICICI Direct](https://www.icicidirect.com/ilearn/futures-and-options/articles/stt-changes-in-budget-2026-what-f-o-traders-should-know). The 0.05% value only coincidentally equals the new futures rate. Options cannot be modelled at all, because there is no premium input and no futures/options split (schemas/portfolio.py:67-73).
- The calculation ignores the side of the trade. `calculate_charges` takes no buy/sell side, yet applies:
  - intraday STT (sell-only),
  - stamp duty (buy-only),
  - DP charges (sell-only, applied here to every delivery trade at a flat ₹13.50 with no GST),
  - all to the same single leg (broker_charges.py:34-40).
  - The delivery probe (₹1,00,000) produced STT ₹100 + stamp ₹15 + DP ₹13.50 on one leg. That is only correct for a round trip if the trade value is half the order. In other words, it is internally inconsistent.
- The exchange transaction rate is a flat 0.00325% for every segment (broker_charges.py:37). NSE equity cash moved from 0.00322% to 0.00297% on 1 Oct 2024 — [Zerodha bulletin](https://zerodha.com/marketintel/bulletin/391488/revision-in-transactions-charges-from-1st-october-2024). Zerodha's current page shows 0.00307% — [Zerodha support](https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/exchange-transaction-charges). The effective date of the 0.00307% figure was not found. Options transaction charges are levied on premium at a much higher rate, and the code does not distinguish them.
- The SEBI fee of 0.0001% (₹10/crore) is correct (broker_charges.py:38). But GST is computed on `brokerage + exchange` only (line 41), while GST at 18% applies to "brokerage, SEBI charges, and transaction charges" — [Zerodha support/charges via search](https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/exchange-transaction-charges). So SEBI fees are wrongly excluded from the GST base.
- The stamp duty rates match the 2020 Indian Stamp Act schedule: delivery 0.015%, intraday 0.003%, futures 0.002% (broker_charges.py:35). Options at 0.003% of premium are not modelled.
- Rate cards: all five brokers have `delivery: '0'` (broker_charges.py:7-11). The cards are explicitly labelled unverified (line 7 note; `calculation_status`, line 59), but several brokers' current delivery brokerage is non-zero. This was not verified in this session; zerodha.com and groww.in pricing pages could not be fetched because of the network allowlist.
- `_fee` applies `min(₹20, raw)` to all intraday cards and treats any rate ≥1 as a flat fee (broker_charges.py:15-21), so the per-broker structure is hard-coded rather than data-driven.

**Precision**
- Internally, Decimal and NUMERIC(24,8)/(24,4)/(24,2) are used consistently (models/portfolio.py:14-15; models/goal.py:14-16).
- The output is float everywhere (money.py:24-26; portfolio.py:36-43; Quote.to_dict, backend/app/providers/market_data.py:19-24).
- `qty` is emitted as `float(qty)`, which loses precision for 8-decimal MF units (tax_calculator.py:49; portfolio.py:36).
- Timestamps are naive UTC (`utc_now_naive`, backend/app/domain/clock.py:4-6), while audit uses tz-aware timestamps (audit.py:16). The mixed conventions make IST reporting error-prone.

**Domain model gaps**
- Each holding has a single average price and a text buy date (models/portfolio.py:14-19). There are no transactions, lots, corporate actions or realised P&L, so XIRR, FIFO tax lots and broker reconciliation are impossible. The docs agree (docs/CAPABILITY_ASSESSMENT.md:41,87).
- `HoldingUpdate` cannot change `buy_date`, `exchange` or `asset_type` (schemas/portfolio.py:30-34).
- Alerts are stored, but nothing evaluates them (watchlist.py:60-81).
- The `Goal.icon` default is an emoji in a String(10) column (models/goal.py:13), while the schema default is 'Goal' (schemas/portfolio.py:38). This is a minor inconsistency.

**Operations**
- `/ready` returns 503 when the database is down (main.py:62-73). `/health` is static.
- There is no structured logging, metrics or tracing.
- `create_all` runs at import time when `AUTO_CREATE_SCHEMA` is true, which is the default in config.py:23 and .env.example:13.
- The SQLite engine uses `check_same_thread=False` with a default pool (backend/app/database.py:12-15).
- docker-compose uses a default Postgres password `nivara-dev-only` (docker-compose.yml:7) and runs migrations in the container start command (line 32).

### Inferences
- The most consequential defects for a credible beta, in order:
  1. The email-case login lockout and duplicate accounts.
  2. The production secret check accepting the template value.
  3. Token storage in localStorage without an SPA CSP.
  4. Tax headline numbers that ignore loss set-off and cess while appearing precise to the paisa.
  5. F&O and side-of-trade statutory charge errors.
- For a product whose whole pitch is "never fabricate", showing a ₹20,000 tax figure on a net-zero gain is a trust problem even with a disclaimer.

### Gaps
- PostgreSQL behaviour for the long `X-Request-ID` was inferred, not executed; no PostgreSQL server was available in this session.
- Current broker tariffs (Zerodha, Groww, Angel One, Upstox, Dhan) and the effective date of NSE's 0.00307% rate could not be confirmed from primary sources, because zerodha.com is outside the session network allowlist.
- The new section number for STCG on listed equity under the Income-tax Act, 2025 (the successor of 111A) was not confirmed.
- The Groww Trading API endpoints and response shapes (`/v1/user/detail`, `/v1/holdings/user`) were not re-verified against live Groww docs in this session.

## 4. Test coverage: actual run results

### Takeaway
The backend suite is small but green: 30 tests pass in about 6 s on SQLite. It is API-journey-heavy and thin on financial-rule correctness. The frontend builds but fails lint, and npm audit fails at high severity. There are no frontend tests and no E2E tests at all.

### Cited Findings
- `cd backend && pip install -r requirements-dev.txt && pytest -q` ran on Python 3.13.18 (CI uses 3.11, per .github/workflows/ci.yml:33). Result: `30 passed in 5.64s`, exit 0. Only SQLite was run; PostgreSQL was not available.
- Test inventory, 331 lines:
  - tests/test_api_journeys.py: 20 tests, lines 10-201. Covers register/login/me, wrong password, bcrypt limit, holdings CRUD and fallback disclosure, cross-user isolation, goals, Nia degradation, Nia history rejection, market auth, unknown broker 404, deactivation, briefing, tax exclusion, WebSocket auth and own-holdings scope, ready/docs headers, the broker catalog, Groww auth, a mocked Groww snapshot, and Motilal configuration.
  - tests/test_financial_precision.py: 4 tests.
  - tests/test_foundations.py: 4 tests.
  - tests/test_tax_and_goals.py: 2 tests.
- Not covered by tests:
  - Email case handling.
  - Loss set-off, cess, buy-date parsing and the holding-period boundary (exactly 365/366 days).
  - Statutory charge values against authoritative examples.
  - Rate limiting.
  - The `X-Request-ID` bound.
  - Watchlist and alert isolation: no test name mentions them, although CAPABILITY_ASSESSMENT line 85 claims they are covered. Only `test_cross_user_isolation` exists (line 50); its scope beyond holdings/goals was not inspected line by line.
  - Nia success-path prompt construction.
  - Groww error paths (non-dict JSON, 401).
  - JWT expiry.
  - The Motilal URL when configured.
- The single session-scoped `TestClient` and shared database across all tests (backend/tests/conftest.py:21-28) create test-order coupling.
- `npm ci` passed (256 packages, 4 s). Deprecation warnings were printed for eslint@8.57.1 ("no longer supported").
- `npm run lint` failed with 2 errors, `react/no-unescaped-entities` at App.jsx:212:42 and 215:94 (LINT_EXIT 1).
- `npm run build` passed: vite v8.3.1, 1944 modules, a 219.25 kB JS bundle (73.33 kB gzip), and 10.19 kB CSS. The assessment reported 160 kB on 30 Sep.
- `npm audit --audit-level=high` failed with 3 high-severity findings (vite and launch-editor; fixes available via `npm audit fix`).
- There is no frontend test runner (no vitest or jest in frontend/package.json) and no Playwright or Cypress.

### Inferences
- HEAD would fail CI in the `frontend` job on two steps, lint and audit. The backend job would likely pass on SQLite. `pip-audit` was not executed in this session.
- Coverage maps to TESTING_STRATEGY's API-integration layer only partially. The "authoritative reference examples" for tax and charges (docs/TESTING_STRATEGY.md:3) do not exist.

### Gaps
- The PostgreSQL test run and the `alembic upgrade/check/downgrade` round trip were not executed in this session.
- No code-coverage percentage was measured, because pytest-cov is not in requirements-dev.txt.

## 5. CI workflow coverage

### Takeaway
CI (.github/workflows/ci.yml) is reasonably well designed for a prototype. It has a backend matrix on SQLite and PostgreSQL, a migration round trip with drift check, pip-audit, frontend lint/build/audit, and gitleaks. It lacks coverage measurement, type and lint checks for Python, container builds and scans, SAST, E2E tests, dependency pinning of actions, and any deploy path. HEAD would currently fail it.

### Cited Findings
- Triggers: `pull_request`, and `push` to main. Permissions are `contents: read` (ci.yml:2-8).
- Backend job:
  - A Postgres 16 service (ci.yml:16-26), Python 3.11 (line 33) and pip install (line 36).
  - `compileall` (line 37).
  - pytest on SQLite (lines 38-39).
  - `alembic upgrade head` / `check` / `downgrade base` / `upgrade head` on PostgreSQL (lines 40-47).
  - pytest on PostgreSQL (lines 48-51).
  - `pip-audit -r requirements.txt` (lines 52-53).
- Frontend job: Node 22, `npm ci`, `lint`, `build`, then `npm audit --audit-level=high` (ci.yml:55-70).
- Secret scan: `gitleaks/gitleaks-action@v2` with full history (ci.yml:72-80).
- Missing:
  - Python linting and type checking (ruff, mypy).
  - Coverage thresholds.
  - SAST (bandit, CodeQL, semgrep).
  - Docker image build and scan (Trivy), even though the Dockerfiles exist.
  - A Python version matrix (Dockerfile 3.11 vs. local 3.13).
  - Frontend unit and E2E tests.
  - OpenAPI contract checks between `src/api/*.js` and the backend.
  - Actions pinned by SHA (`@v4`, `@v2` tags only).
  - `pip-audit` installed unpinned (backend/requirements-dev.txt:3).
  - Dependabot or Renovate configuration.
  - Staging deploy, smoke test and rollback, which the tracker itself names (docs/PRODUCTION_READINESS_TRACKER.md:20).
- PHASE-2 notes that CI "still need[s] to run in GitHub before [it] count[s] as verified release evidence" (docs/PHASE-2-IMPLEMENTATION-REPORT.md:15).

### Inferences
- Because frontend `npm audit --audit-level=high` blocks the job, new dev-dependency advisories will break CI regularly, as happened between 30 Sep and now. This calls for an automated dependency-update bot.

### Gaps
- GitHub Actions run history was not inspected.

## 6. Top engineering priorities: prototype to credible beta

### Takeaway
Fix the trust-critical correctness and security defects first. Next, redesign the portfolio around transactions and connect the broker snapshot to it. Then wire the frontend to the existing APIs, with a licensed data decision, caching, and evaluated Nia grounding. Each step needs tests against authoritative Indian tax and charge examples.

### Cited Findings (evidence behind each priority)
1. **Restore CI green.** Fix the 2 lint errors (App.jsx:212,215) and upgrade vite (npm audit high). Correct the stale verification claims in docs/CAPABILITY_ASSESSMENT.md:81,85 and README.md:17,21.
2. **Auth hardening.**
   - Normalise emails to lowercase on register and login, and add a unique index on the lowercased value (auth.py:22,42; verified defect).
   - Reject known template secrets and require high-entropy keys (config.py:43; .env.example:2).
   - Move tokens out of localStorage to httpOnly SameSite cookies with CSRF protection, or add a strict CSP to nginx (client.js:12; nginx.conf:6-8).
   - Add `jti`-based revocation, refresh tokens and logout (utils/auth.py:31-34).
   - Add a login throttle per account and per IP.
3. **Shared rate limiter and request hygiene.** Use a Redis-backed limiter keyed on user plus trusted-proxy client IP, with per-endpoint limits for login, Groww and Nia (request_context.py:22-42). Bound and validate `X-Request-ID` to 64 characters (request_context.py:13; models/audit.py:13).
4. **Tax and charges correctness.** Implement:
   - STCL/LTCL set-off and the cess (tax_calculator.py:56-60).
   - Strict date parsing, with no 400-day default (lines 33-36).
   - Classification of ETFs by underlying.
   - A note on the Income-tax Act, 2025 references.
   - For charges: a buy/sell side, futures vs. options with premium input, the 2026 F&O STT rates (0.05% / 0.15%), current NSE/BSE transaction rates by segment, SEBI fees in the GST base, and DP charges on sells only (broker_charges.py:34-42).
   - Move rates into versioned, dated rule tables with effective dates and source citations, and add fixture tests from published broker contract-note examples.
5. **Transaction-based portfolio schema.** This means transactions, lots, ISIN-keyed instruments and corporate actions (the gap in models/portfolio.py:6-24; docs/CAPABILITY_ASSESSMENT.md:89). Then persist and reconcile Groww snapshots, which already return ISIN, quantity and average price (broker_connections.py:105-113), into it. This needs an encrypted token store, consent records and revocation (docs/BROKER_CONNECTIONS.md:52). Motilal needs a callback with a `state` parameter (broker_connections.py:54-58).
6. **Market-data layer.**
   - Make a licensed provider decision (tracker "Blocked", docs/PRODUCTION_READINESS_TRACKER.md:24).
   - Wire up a real TTL cache, using the dead `utils/cache.py` or Redis.
   - Batch quotes, and make the yfinance calls async or offloaded (portfolio.py:26-27; yfinance_provider.py:14-32).
   - Honour `exchange`, and use the exchange timestamp for `as_of`.
7. **Frontend journeys.** Use the existing `portfolioAPI`/`marketAPI` modules, which are currently unused (frontend/src/api/portfolio.js; market.js). Replace `demoHoldings` and the scripted Nia (App.jsx:11-16,64-73) with backend calls. Add a router, Account navigation, error and stale-data states, and Vitest/Playwright tests.
8. **Nia.**
   - Use async DB access or `run_in_threadpool` for queries (ai_chat.py:65-66,85-87).
   - Use a shared HTTP client and the official SDK.
   - Add per-user quotas and cost telemetry.
   - Add retrieval with citations, allowlisted server-authorised tools (docs/SECURITY_MODEL.md:5), an output policy check for advice language, and an evaluation set including prompt-injection cases (docs/TESTING_STRATEGY.md:7).
   - Add history deletion and retention controls.
9. **Observability and audit.**
   - Structured JSON logs with request IDs.
   - Metrics and traces.
   - Audit coverage of all financial mutations and profile changes (auth.py:62-68; portfolio.py:89-121; goals.py; watchlist.py).
   - Retention and integrity controls.
10. **CI/CD.**
    - Add ruff, mypy and bandit/CodeQL.
    - Add coverage gates.
    - Build and Trivy-scan the containers.
    - Pin actions by SHA and add Dependabot.
    - Add a staging deploy with smoke tests and a backup/restore drill (tracker lines 22-25).
11. **Regulatory and product.**
    - Obtain the SEBI IA/RA review the README says has not happened (README.md:73).
    - Choose a licence (README.md:77).
    - Consider the Account Aggregator route for read-only holdings, rather than pasting daily broker tokens. This is an inference; the AA framework was not researched in this session.

### Inferences
- Priorities 1–4 are small, high-leverage changes, plausibly days of work. Priority 5 is the architectural keystone, because tax, XIRR, imports and reconciliation all depend on it. Without priority 6, any real-user load will make portfolio pages slow, at N sequential network calls per page.

### Gaps
- No effort estimates or team-capacity information exist in the repository. The ordering above is an engineering judgement based on the evidence cited.
