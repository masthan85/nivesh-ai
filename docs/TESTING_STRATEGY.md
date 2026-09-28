# Testing strategy

Financial correctness tests are the highest priority. Portfolio valuation, realised and unrealised P&L, percentage returns, currency conversion, fees, broker costs, tax rules, corporate actions and scenario calculations should have deterministic fixture-based tests with boundary cases and authoritative reference examples.

API integration tests should cover registration, login, expired/invalid tokens, cross-user access attempts, holdings CRUD, watchlists, goals, provider failures and Nia failure modes. End-to-end tests should cover the same journeys through the browser with explicit checks for loading, empty, stale-data and error states.

Security testing should include dependency and secret scanning, authorization tests, injection cases, rate-limit/abuse cases and AI-specific prompt-injection/tool-authorization tests. Production deployment verification should test health/readiness, migration success, rollback and provider degradation.
