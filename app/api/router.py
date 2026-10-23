from fastapi import APIRouter

from app.api.v1.endpoints import router as health_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.events import router as events_router
from app.api.v1.subscriptions import router as subscriptions_router
from app.api.v1.attempts import router as attempts_router
api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(webhooks_router, prefix="/api/v1")
api_router.include_router(events_router, prefix="/api/v1")


api_router.include_router(
    subscriptions_router,
    prefix="/api/v1",
)



api_router.include_router(attempts_router, prefix="/api/v1")