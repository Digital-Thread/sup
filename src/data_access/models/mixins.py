from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, unique=True)]


class IntIdPkMixin:
    id: Mapped[pk]


class UUIDPkMixin:
    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.uuid_generate_v4(),
    )


class DatetimeFieldsMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
