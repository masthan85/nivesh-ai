# Security verification model

Nivara AI is being designed as a financial application containing sensitive portfolio and identity data. Application controls should be verified against OWASP ASVS 5.0 rather than treated as a branding claim. The current build establishes only an initial baseline: explicit CORS origins, production secret validation, security headers, server-side ownership checks already present in core portfolio routes, schema validation, and safer AI-provider failure handling.

The AI layer requires a separate verification gate using OWASP AISVS. Nia must never bypass application authorization. Retrieved text and external content must be considered untrusted. Tool calls must be allowlisted, scoped to the authenticated user, and re-authorized deterministically on the server. Model output is never authority for a financial transaction or access-control decision.

Priority threat scenarios include credential theft, cross-user portfolio access, token theft, excessive API requests, malicious market/news payloads, indirect prompt injection, prompt-based privilege escalation, sensitive-data leakage, fabricated financial claims, tool-call manipulation, and provider compromise or outage.
