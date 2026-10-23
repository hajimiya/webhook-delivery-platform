from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Event
from app.db.session import get_db
from app.schemas.event import EventCreate, EventResponse

from sqlalchemy import select

from app.db.models import Webhook, WebhookSubscription
from app.services.delivery import deliver_event

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    event = Event(
        event_type=data.event_type,
        payload=data.payload,
        idempotency_key=data.idempotency_key,
    )
    db.add(event)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Idempotency key already exists",
        )

    db.refresh(event)

    subscriptions = db.scalars(
        select(WebhookSubscription).where(
            WebhookSubscription.event_type == event.event_type
        )
    ).all()

    for subscription in subscriptions:
        webhook = db.get(Webhook, subscription.webhook_id)

        if webhook is not None and webhook.is_active:
            deliver_event(db, event, webhook)

    return event


@router.get("", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.scalars(
        select(Event).order_by(Event.created_at.desc())
    ).all()