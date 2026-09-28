# Nivara AI target architecture

The near-term architecture remains a modular monolith. The React client talks to a versioned FastAPI application. FastAPI owns authentication, application services and domain rules. Domain modules isolate portfolio, goals, taxes, broker costs, risk and alerts. External market, fundamentals, news and AI providers sit behind adapters. PostgreSQL is the production system of record, Redis is reserved for cache and short-lived coordination, and asynchronous workers are introduced only for workloads such as alerts, imports and briefings.

Financial calculations remain deterministic application services and must not be delegated to an LLM. Nia orchestrates retrieval and approved tools, then interprets sourced results. Every external datum should carry source, timestamp, market timezone and freshness classification. Core portfolio access must continue working when AI or news providers fail.
