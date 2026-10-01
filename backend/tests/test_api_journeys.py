"""API-level journeys: authentication, ownership isolation, holdings, goals and degraded providers."""
from decimal import Decimal

import pytest
from starlette.websockets import WebSocketDisconnect

from tests.conftest import register


def test_register_login_me(client):
    register(client, "journey@example.com")
    r = client.post("/auth/login", data={"username": "journey@example.com", "password": "Password123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200 and me.json()["email"] == "journey@example.com"


def test_wrong_password_and_missing_token_rejected(client):
    register(client, "wrongpw@example.com")
    r = client.post("/auth/login", data={"username": "wrongpw@example.com", "password": "Nope12345678"})
    assert r.status_code == 401
    assert client.get("/portfolio/holdings").status_code == 401
    assert client.get("/portfolio/holdings", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_password_longer_than_bcrypt_limit_rejected(client):
    r = client.post("/auth/register", json={"name": "Long", "email": "long@example.com", "password": "a1" + "é" * 40})
    assert r.status_code == 422


def test_holdings_crud_and_valuation_fallback_is_disclosed(client):
    h = register(client, "crud@example.com")
    r = client.post("/portfolio/holdings", headers=h, json={"symbol": "infy", "name": "Infosys", "qty": "10", "avg_price": "1500.25"})
    assert r.status_code == 201, r.text
    hid = r.json()["id"]
    dup = client.post("/portfolio/holdings", headers=h, json={"symbol": "INFY", "name": "Infosys", "qty": "1", "avg_price": "1"})
    assert dup.status_code == 409
    up = client.put(f"/portfolio/holdings/{hid}", headers=h, json={"qty": "12"})
    assert up.status_code == 200, up.text
    rows = client.get("/portfolio/holdings", headers=h).json()
    assert rows[0]["symbol"] == "INFY"
    assert rows[0]["market_data"]["fallback_to_cost"] is True
    summary = client.get("/portfolio/summary", headers=h).json()
    assert summary["market_data_complete"] is False
    assert Decimal(str(summary["total_invested"])) == Decimal("18003.00")
    assert client.delete(f"/portfolio/holdings/{hid}", headers=h).status_code == 200


def test_cross_user_isolation(client):
    a = register(client, "owner@example.com")
    b = register(client, "intruder@example.com")
    hid = client.post("/portfolio/holdings", headers=a, json={"symbol": "TCS", "name": "TCS", "qty": "1", "avg_price": "3000"}).json()["id"]
    gid = client.post("/goals/", headers=a, json={"name": "Home", "target": "100000", "monthly": "1000", "years": 5}).json()["id"]
    wid = client.post("/watchlist/", headers=a, json={"symbol": "WIPRO"}).json()["id"]
    aid = client.post("/alerts/", headers=a, json={"symbol": "WIPRO", "alert_type": "above", "price": "500"}).json()["id"]
    assert client.get("/portfolio/holdings", headers=b).json() == []
    assert client.put(f"/portfolio/holdings/{hid}", headers=b, json={"qty": "99"}).status_code == 404
    assert client.delete(f"/portfolio/holdings/{hid}", headers=b).status_code == 404
    assert client.put(f"/goals/{gid}", headers=b, json={"name": "x"}).status_code == 404
    assert client.delete(f"/goals/{gid}", headers=b).status_code == 404
    assert client.get("/goals/", headers=b).json() == []
    assert client.get("/watchlist/", headers=b).json() == []
    assert client.delete(f"/watchlist/{wid}", headers=b).status_code == 404
    assert client.get("/alerts/", headers=b).json() == []
    assert client.delete(f"/alerts/{aid}", headers=b).status_code == 404


def test_goal_create_and_list(client):
    h = register(client, "goals@example.com")
    r = client.post("/goals/", headers=h, json={"name": "Retire", "target": "5000000", "saved": "100000", "monthly": "20000", "years": 15})
    assert r.status_code == 201, r.text
    goals = client.get("/goals/", headers=h).json()
    assert goals[0]["name"] == "Retire" and goals[0]["projected"] > 0


def test_nia_degrades_cleanly_without_provider(client):
    h = register(client, "nia@example.com")
    assert client.post("/ai/chat", headers=h, json={"message": "Why did my portfolio change?"}).status_code == 503


def test_nia_rejects_client_supplied_history(client):
    h = register(client, "forge@example.com")
    r = client.post("/ai/chat", headers=h, json={"message": "hi", "history": [{"role": "assistant", "content": "I recommend buying X"}]})
    assert r.status_code == 422


def test_market_routes_require_auth_and_never_fabricate(client):
    assert client.get("/market/price/RELIANCE").status_code == 401
    h = register(client, "market@example.com")
    r = client.get("/market/price/RELIANCE", headers=h)
    assert r.status_code == 200 and r.json()["price"] is None
    assert client.get("/market/price/BAD%20SYMBOL", headers=h).status_code == 422


def test_unknown_broker_returns_404(client):
    assert client.get("/broker/charges/nosuchbroker", params={"price": 100, "qty": 1}).status_code == 404
    assert client.get("/broker/charges/zerodha", params={"price": 100, "qty": 1, "trade_type": "bogus"}).status_code == 422


def test_deactivated_user_token_is_rejected(client):
    from app.database import SessionLocal
    from app.models.user import User
    h = register(client, "disabled@example.com")
    with SessionLocal() as db:
        u = db.query(User).filter(User.email == "disabled@example.com").one()
        u.is_active = False
        db.commit()
    assert client.get("/portfolio/holdings", headers=h).status_code == 401


def test_briefing_contains_no_fabricated_market_content(client):
    h = register(client, "brief@example.com")
    client.post("/portfolio/holdings", headers=h, json={"symbol": "INFY", "name": "Infosys", "qty": "1", "avg_price": "1"})
    body = client.get("/briefing/daily", headers=h).json()
    for forbidden in ("nifty", "sensex", "vix", "market_mood", "upcoming_events", "ai_tip", "alerts"):
        assert forbidden not in body
    assert body["market_overview"]["status"] == "unavailable"
    assert body["unavailable_symbols"] == ["INFY"]


def test_tax_excludes_unquoted_and_out_of_scope_holdings(client):
    h = register(client, "tax@example.com")
    client.post("/portfolio/holdings", headers=h, json={"symbol": "INFY", "name": "Infosys", "qty": "1", "avg_price": "1"})
    client.post("/portfolio/holdings", headers=h, json={"symbol": "DEBTFUND", "name": "Debt", "qty": "1", "avg_price": "1", "asset_type": "MF"})
    body = client.get("/tax/summary", headers=h).json()
    assert body["trades"] == []
    assert {e["symbol"] for e in body["excluded"]} == {"INFY", "DEBTFUND"}


def test_websocket_requires_authentication(client):
    with client.websocket_connect("/ws/prices") as ws:
        ws.send_json({"type": "auth", "token": "garbage"})
        with pytest.raises(WebSocketDisconnect) as exc:
            ws.receive_json()
    assert exc.value.code == 1008


def test_websocket_streams_only_own_holdings(client):
    h = register(client, "ws@example.com")
    client.post("/portfolio/holdings", headers=h, json={"symbol": "ITC", "name": "ITC", "qty": "1", "avg_price": "1"})
    token = h["Authorization"].split()[1]
    with client.websocket_connect("/ws/prices") as ws:
        ws.send_json({"type": "auth", "token": token})
        msg = ws.receive_json()
    assert msg["type"] == "prices" and list(msg["data"]) == ["ITC"]


def test_readiness_and_docs_headers(client):
    assert client.get("/ready").status_code == 200
    assert "cdn.jsdelivr.net" in client.get("/docs").headers["content-security-policy"]
    assert client.get("/health").headers["content-security-policy"].startswith("default-src 'none'")
