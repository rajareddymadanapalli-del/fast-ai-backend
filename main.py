from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import os

# Sentry Setup (Error Tracking)
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FastApiIntegration()])

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online", "monitoring": "active"}

@app.get("/sentry-debug")
async def trigger_error():
    # This tests if Sentry captures unhandled exceptions
    division_by_zero = 1 / 0
