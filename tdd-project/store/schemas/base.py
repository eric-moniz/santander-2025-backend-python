from datetime import datetime
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

from store.core.datetime_utils import utc_now


class BaseSchemaMixin(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
