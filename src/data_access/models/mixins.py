from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, unique=True)]


class IntIdPkMixin:
    id: Mapped[pk]


class DatetimeFieldsMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
