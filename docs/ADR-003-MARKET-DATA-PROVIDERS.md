# ADR-003: Replaceable market-data providers

## Decision

Core portfolio logic will depend on a market-data provider interface rather than directly importing a vendor SDK. Every quote must carry source, timestamp, freshness state and whether the feed is considered live.

The existing yfinance integration is retained only as a development adapter and is explicitly labelled non-production. When a production provider is selected, its licensing and technical characteristics must be reviewed before activation.

## Consequences

Provider outages can be represented as unavailable data instead of silently substituting fabricated prices. Portfolio routes may explicitly fall back to cost basis for display continuity, but must disclose that the resulting figure is not a live valuation.
