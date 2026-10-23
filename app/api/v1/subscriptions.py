from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models import Webhook, WebhookSubscription
from app.db.session import get_db
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subscription(
    data: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    webhook = db.get(Webhook, data.webhook_id)

    if webhook is None:
        raise HTTPException(status_code=404, detail="Webhook not found")

    subscription = WebhookSubscription(
        webhook_id=data.webhook_id,
        event_type=data.event_type,
    )
    db.add(subscription)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This subscription already exists",
        )

    db.refresh(subscription)
    return subscription


@router.get("", response_model=list[SubscriptionResponse])
def list_subscriptions(db: Session = Depends(get_db)):
    return db.scalars(
        select(WebhookSubscription).order_by(
            WebhookSubscription.created_at.desc()
        )
    ).all()


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(
    subscription_id: UUID,
    db: Session = Depends(get_db),
):
    subscription = db.get(WebhookSubscription, subscription_id)

    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(subscription)
    db.commit()