from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import DatetimeFieldsMixin, UUIDPkMixin


class User(Base, DatetimeFieldsMixin, UUIDPkMixin):
    __tablename__ = 'users'  # type: ignore

    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
