from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from app.config import settings


GROWW_API_BASE_URL = "https://api.groww.in"
GROWW_DOCS_URL = "https://groww.in/trade-api/docs"
MOTILAL_DOCS_URL = "https://invest.motilaloswal.com/moAPI/APIDocumentation/Introduction"
MOTILAL_LOGIN_URL = "https://invest.motilaloswal.com/OpenAPI/Login.aspx"


class BrokerConnectionError(RuntimeError):
    pass


def provider_catalog() -> list[dict[str, Any]]:
    motilal_configured = bool(settings.MOTILAL_API_KEY.strip())
    return [
        {
            "id": "groww",
            "name": "Groww",
            "status": "available",
            "connection_mode": "user_access_token",
            "read_only": True,
            "supports": ["Indian equity holdings", "positions", "user profile"],
            "limitations": [
                "Current Nivara build verifies a user-provided Groww access token and returns a read-only snapshot.",
                "Nivara does not persist the Groww token in this build.",
                "Groww access tokens expire daily at 6:00 AM according to Groww's current API documentation.",
            ],
            "docs_url": GROWW_DOCS_URL,
        },
        {
            "id": "motilal-oswal",
            "name": "Motilal Oswal",
            "status": "configured" if motilal_configured else "setup_required",
            "connection_mode": "broker_redirect",
            "read_only": True,
            "supports": ["DP holdings", "positions", "account information"],
            "limitations": [
                "A Nivara/MOFSL API app key and registered redirect URL are required before the broker redirect can complete inside Nivara.",
                "No broker password should ever be collected by Nivara; authentication belongs on the Motilal Oswal portal.",
            ],
            "docs_url": MOTILAL_DOCS_URL,
        },
    ]


def motilal_login_url() -> str | None:
    api_key = settings.MOTILAL_API_KEY.strip()
    if not api_key:
        return None
    return f"{MOTILAL_LOGIN_URL}?apikey={api_key}"


def _groww_headers(access_token: str) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "X-API-VERSION": "1.0",
    }


def _payload(response: httpx.Response, label: str) -> dict[str, Any]:
    try:
        body = response.json()
    except ValueError as exc:
        raise BrokerConnectionError(f"Groww returned an unreadable {label} response") from exc
    if response.status_code >= 400:
        raise BrokerConnectionError(f"Groww rejected the {label} request")
    if str(body.get("status", "")).upper() not in {"SUCCESS", ""}:
        raise BrokerConnectionError(f"Groww could not complete the {label} request")
    data = body.get("payload", {})
    return data if isinstance(data, dict) else {}


def fetch_groww_snapshot(access_token: str) -> dict[str, Any]:
    token = access_token.strip()
    if len(token) < 20:
        raise BrokerConnectionError("The Groww access token appears incomplete")

    headers = _groww_headers(token)
    try:
        with httpx.Client(timeout=12.0, follow_redirects=False) as client:
            profile_response = client.get(f"{GROWW_API_BASE_URL}/v1/user/detail", headers=headers)
            holdings_response = client.get(f"{GROWW_API_BASE_URL}/v1/holdings/user", headers=headers)
    except httpx.HTTPError as exc:
        raise BrokerConnectionError("Groww is temporarily unreachable") from exc

    profile = _payload(profile_response, "profile")
    holdings_payload = _payload(holdings_response, "holdings")
    raw_holdings = holdings_payload.get("holdings", [])
    if not isinstance(raw_holdings, list):
        raw_holdings = []

    holdings: list[dict[str, Any]] = []
    for row in raw_holdings:
        if not isinstance(row, dict):
            continue
        holdings.append({
            "isin": row.get("isin"),
            "symbol": row.get("trading_symbol"),
            "quantity": row.get("quantity"),
            "average_price": row.get("average_price"),
            "pledge_quantity": row.get("pledge_quantity"),
            "t1_quantity": row.get("t1_quantity"),
            "demat_free_quantity": row.get("demat_free_quantity"),
        })

    return {
        "provider": "groww",
        "status": "connected_snapshot",
        "read_only": True,
        "persisted_token": False,
        "source": "Groww Trading API",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "profile": {
            "vendor_user_id": profile.get("vendor_user_id"),
            "ucc": profile.get("ucc"),
            "nse_enabled": profile.get("nse_enabled"),
            "bse_enabled": profile.get("bse_enabled"),
            "ddpi_enabled": profile.get("ddpi_enabled"),
            "active_segments": profile.get("active_segments", []),
        },
        "holdings": holdings,
        "holding_count": len(holdings),
        "notice": "Snapshot only. Nivara did not store the Groww access token; reconnect to refresh after the current session or token expiry.",
    }
