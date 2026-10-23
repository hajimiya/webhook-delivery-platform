import httpx
from sqlalchemy.orm import Session

from app.db.models import DeliveryAttempt, Event, Webhook


def deliver_event(
    db: Session,
    event: Event,
    webhook: Webhook,
) -> DeliveryAttempt:
    attempt = DeliveryAttempt(
        event_id=event.id,
        webhook_id=webhook.id,
        status="pending",
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                webhook.url,
                json={
                    "id": str(event.id),
                    "event_type": event.event_type,
                    "payload": event.payload,
                },
                headers={"Content-Type": "application/json"},
            )

        attempt.response_status_code = response.status_code
        attempt.response_body = response.text[:2000]
        attempt.status = (
            "success" if 200 <= response.status_code < 300 else "failed"
        )

    except httpx.HTTPError as exc:
        attempt.status = "failed"
        attempt.error_message = str(exc)[:2000]

    db.commit()
    db.refresh(attempt)
    return attempt