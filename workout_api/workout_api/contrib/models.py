import uuid
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), default=uuid4, nullable=False
    )
