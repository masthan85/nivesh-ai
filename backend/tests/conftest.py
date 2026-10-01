"""Integration-test setup: isolated database, no network market data, no AI key.

TEST_DATABASE_URL may point at a PostgreSQL database. It must be a dedicated test
database: every table in it is dropped and recreated at the start of the run.
"""
import os
import tempfile

_db_dir = tempfile.mkdtemp(prefix="nivara-test-")
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", f"sqlite:///{_db_dir}/test.db")
os.environ["MARKET_DATA_MODE"] = "unavailable"
os.environ["ANTHROPIC_API_KEY"] = ""
os.environ["AUTO_CREATE_SCHEMA"] = "false"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-123456"
os.environ["RATE_LIMIT_PER_MINUTE"] = "10000"

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    from app.database import Base, engine
    from app.main import app

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestClient(app)


def register(client, email, password="Password123"):
    r = client.post("/auth/register", json={"name": "Test User", "email": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
