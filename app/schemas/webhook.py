from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class WebhookCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    url: HttpUrl
    secret: str = Field(min_length=16, max_length=255)


class WebhookResponse(BaseModel):
    id: UUID
    name: str
    url: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)