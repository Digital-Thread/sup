from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import DatetimeFieldsMixin, UUIDPkMixin


class User(Base, DatetimeFieldsMixin, UUIDPkMixin):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    username_tg: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_tg: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_gmeet: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_gitlab: Mapped[str] = mapped_column(String(50), nullable=True)
    nick_github: Mapped[str] = mapped_column(String(50), nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
