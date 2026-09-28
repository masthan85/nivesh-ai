# Environment and secrets

Use the checked-in `.env.example` files only as templates. Never commit populated `.env` files. Production must use a secret manager or deployment-platform secret store. The backend rejects the default secret when `ENVIRONMENT=production` and does not allow wildcard CORS origins.

`SEED_DEMO_DATA` is false by default. Demo data may be enabled only in isolated development environments and must remain visibly labelled as simulated information.
