# Broker Connections — Groww and Motilal Oswal

Verified against official provider documentation on 1 October 2026.

## Design principles

- Nivara never collects broker passwords.
- Connections are read-only first.
- Tokens are treated as secrets and are not written to logs.
- The first Groww implementation validates a user-provided access token and returns a live account/holdings snapshot. The token is not persisted.
- Broker data is not merged into the canonical Nivara portfolio until instrument mapping, reconciliation, and licensed valuation data are in place.

## Groww

Official docs: https://groww.in/trade-api/docs

Groww currently documents access-token, API-key/secret, and TOTP authentication for its Trading API. The current Nivara build uses the simplest read-only path: the user generates a current Groww access token and pastes only that token into Nivara.

Nivara then calls:

- `GET https://api.groww.in/v1/user/detail`
- `GET https://api.groww.in/v1/holdings/user`

Required headers include the Bearer access token and `X-API-VERSION: 1.0`.

Groww states that access tokens expire daily at 6:00 AM. Because this Nivara build intentionally does not store the token, the user reconnects when a new snapshot is needed.

## Motilal Oswal

Official docs: https://invest.motilaloswal.com/moAPI/APIDocumentation/Introduction

Motilal Oswal documents a broker-hosted login flow using an API app key and a registered redirect URL. This is the preferred pattern because the customer enters client code, password, OTP, and 2FA only on the Motilal Oswal domain.

Set the following in `backend/.env` after obtaining the appropriate MOFSL app/vendor credentials:

```env
MOTILAL_API_KEY=your_mofsl_app_key
```

The current Nivara implementation can generate the official broker-login URL but does not yet persist the returned auth/access token or automatically sync MOFSL holdings. Complete callback handling requires a registered Nivara redirect URL and provider onboarding/commercial approval where applicable.

## Local testing

1. Start Nivara with Docker Compose.
2. Create or sign in to a Nivara account from **Account**.
3. Open **Connections**.
4. For Groww, generate a current Trading API access token in Groww and use **Connect Groww**.
5. Nivara should display the returned user profile and read-only holdings snapshot.

## Production follow-up

Before persisting broker sessions in production, add a dedicated encrypted connection store backed by a managed secrets/KMS design, revocation, consent history, token rotation/expiry handling, provider-health monitoring, and reconciliation into the canonical instrument/transaction model.
