# Database migrations

New environments should set `AUTO_CREATE_SCHEMA=false` and run `alembic upgrade head` before starting the API. The current baseline migration creates the production-oriented schema with precision-safe financial columns and the audit-event table.

The repository also contains a prototype SQLite database created before the Alembic baseline. Do not apply the baseline directly over an irreplaceable copy of that file. Back it up first and rehearse data movement into a clean migrated database. Production deployment should use PostgreSQL and migrations rather than SQLAlchemy `create_all`.
