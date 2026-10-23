
from fastapi import APIRouter

router = APIRouter()


@router.get("/health/live", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "alive"}
