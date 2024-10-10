from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .category import Category
    from .user import User
    from .workspace import Workspace


class Meet(Base, IntIdPkMixin, DatetimeFieldsMixin):
    name: Mapped[str]
    meet_at: Mapped[datetime]
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspace.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    assigned_to: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    participants: Mapped[list['Participant']] = relationship(
        cascade='all, delete-orphan', back_populates='meet', lazy='raise_on_sql'
    )

    owner: Mapped['User'] = relationship(
        'User', foreign_keys=[owner_id], back_populates='owned_meetings'
    )

    assigned: Mapped['User'] = relationship(
        'User', foreign_keys=[assigned_to], back_populates='assigned_meetings'
    )

    workspace: Mapped['Workspace'] = relationship(
        'Workspace', foreign_keys=[workspace_id], back_populates='meets', lazy='raise_on_sql'
    )

    # TODO: Decide about cascade delete or not
    category: Mapped['Category'] = relationship('Category', back_populates='meets', lazy='joined')


class Participant(Base, IntIdPkMixin, DatetimeFieldsMixin):
    meet_id: Mapped[int] = mapped_column(ForeignKey('meet.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    status: Mapped[str]

    user: Mapped['User'] = relationship('User', back_populates='participations', lazy='joined')
    meet: Mapped['Meet'] = relationship('Meet', back_populates='participants', lazy='raise_on_sql')

    __table_args__ = (UniqueConstraint('meet_id', 'user_id'),)
