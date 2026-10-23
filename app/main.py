
from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="Webhook Delivery Platform",
    description="A reliable webhook delivery and event processing platform.",
    version="0.1.0",
)

app.include_router(api_router)
