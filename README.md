
# fither-forward-strava (Starter)

A minimal FastAPI service for Strava OAuth callback placeholder and Webhook verify/ingest endpoints.

## Endpoints
- `GET /` – health
- `GET /webhook/strava` – verification (responds with `{ "hub.challenge": ... }` when tokens match)
- `POST /webhook/strava` – event receiver (responds `200 OK` immediately)
- `GET /oauth/strava/callback` – placeholder OAuth callback

## Environment variables required
- `STRAVA_CLIENT_ID` – your app client id
- `STRAVA_CLIENT_SECRET` – your app client secret
- `STRAVA_VERIFY_TOKEN` – any random string you also use when creating a webhook subscription
- `BASE_URL` (optional) – your public base url

## Run locally
```bash
export STRAVA_CLIENT_ID=123
export STRAVA_CLIENT_SECRET=abc
export STRAVA_VERIFY_TOKEN=STRAVA
uvicorn main:app --reload --port 8000
```

