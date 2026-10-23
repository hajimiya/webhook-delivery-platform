from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DeliveryAttempt
from app.db.session import get_db

router = APIRouter(prefix="/attempts", tags=["Delivery Attempts"])


class AttemptResponse(BaseModel):
    id: UUID
    event_id: UUID
    webhook_id: UUID
    status: str
    response_status_code: int | None
    response_body: str | None
    error_message: str | None
    attempted_at: datetime

    model_config = ConfigDict(from_attributes=True)


@router.get("", response_model=list[AttemptResponse])
def list_attempts(db: Session = Depends(get_db)):
    return db.scalars(
        select(DeliveryAttempt).order_by(
            DeliveryAttempt.attempted_at.desc()
        )
    ).all()