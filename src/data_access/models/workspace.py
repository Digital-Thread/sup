from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .category import Category
from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .meet import Meet
    from .user import User


class Workspace(Base, IntIdPkMixin, DatetimeFieldsMixin):
    name: Mapped[str]
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    owner: Mapped['User'] = relationship(
        'User', foreign_keys=[owner_id], back_populates='workspaces'
    )

    meets: Mapped[list['Meet']] = relationship(
        cascade='all, delete-orphan', back_populates='workspace', lazy='raise_on_sql'
    )
    categories: Mapped[list['Category']] = relationship(
        cascade='all, delete-orphan', back_populates='workspace', lazy='raise_on_sql'
    )
