
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
import os

app = FastAPI()

# --- Config ---
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL", "")  # optional public base URL of this service
VERIFY_TOKEN = os.getenv("STRAVA_VERIFY_TOKEN", "STRAVA")  # can be any random string

@app.get("/")
async def root():
    msg = {
        "status": "ok",
        "service": "fither-forward-strava",
        "docs": "/docs",
        "webhook_verify": "/webhook/strava (GET)",
        "webhook_events": "/webhook/strava (POST)",
        "oauth_callback": "/oauth/strava/callback",
    }
    return msg

# --- Webhook verification (GET) ---
@app.get("/webhook/strava")
async def verify_webhook(mode: str | None = None,
                         hub_challenge: str | None = None,
                         hub_verify_token: str | None = None,
                         **kwargs):
    # Strava sends hub.mode=subscribe & hub.challenge during verification
    if mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return JSONResponse({"hub.challenge": hub_challenge})
    raise HTTPException(status_code=403, detail="Forbidden")

# --- Webhook events (POST) ---
@app.post("/webhook/strava")
async def webhook_events(req: Request):
    # Must ACK within 2s
    try:
        payload = await req.json()
    except Exception:
        payload = {}
    # In production: enqueue a background task to fetch activity details
    return PlainTextResponse("OK", status_code=200)

# --- OAuth callback placeholder ---
@app.get("/oauth/strava/callback")
async def oauth_callback(code: str | None = None, error: str | None = None):
    if error:
        return PlainTextResponse(f"Strava error: {error}", status_code=400)
    # In production: exchange code for access_token using /oauth/token
    # Keep this placeholder route so redirect_uri checks pass while we finish setup.
    return PlainTextResponse("Authorization received. You can close this window.")

