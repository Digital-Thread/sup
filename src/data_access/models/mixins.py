import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, unique=True)]
pk_uuid = Annotated[
    uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
]


class IntIdPkMixin:
    id: Mapped[pk]


class UUIDPkMixin:
    id: Mapped[pk_uuid]


class DatetimeFieldsMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
