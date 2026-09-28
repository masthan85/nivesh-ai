# ADR-002: Decimal and NUMERIC for financial values

## Decision

Nivara AI will represent monetary values, quantities requiring fractional precision, fees, tax amounts and deterministic financial calculations with Python `Decimal` and SQL `NUMERIC`. Binary floating-point values are permitted only at presentation boundaries where a consumer explicitly requires JSON numbers.

## Why

Portfolio valuation, P&L, brokerage and tax calculations are financially consequential. Binary floating-point arithmetic can accumulate representation errors and creates avoidable reconciliation risk. Centralising conversion and rounding rules provides predictable behaviour and testability.

## Consequences

Database migrations use precision-aware columns. API schemas accept Decimal-compatible values. Services must avoid converting to float during calculation. Production tax and brokerage outputs still require independent validation against current authoritative rules; precision does not establish regulatory correctness.
