
from fastapi import FastAPI

app = FastAPI(
    title="Webhook Delivery Platform",
    description="A reliable webhook delivery and event processing platform.",
    version="0.1.0",
)


@app.get("/health/live", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "alive"}
