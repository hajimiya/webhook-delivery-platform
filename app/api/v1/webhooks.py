from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Webhook
from app.db.session import get_db
from app.schemas.webhook import WebhookCreate, WebhookResponse

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post(
    "",
    response_model=WebhookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_webhook(
    data: WebhookCreate,
    db: Session = Depends(get_db),
):
    webhook = Webhook(
        name=data.name,
        url=str(data.url),
        secret=data.secret,
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


@router.get("", response_model=list[WebhookResponse])
def list_webhooks(db: Session = Depends(get_db)):
    return db.scalars(
        select(Webhook).order_by(Webhook.created_at.desc())
    ).all()


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_webhook(
    webhook_id: UUID,
    db: Session = Depends(get_db),
):
    webhook = db.get(Webhook, webhook_id)

    if webhook is None:
        raise HTTPException(status_code=404, detail="Webhook not found")

    db.delete(webhook)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)