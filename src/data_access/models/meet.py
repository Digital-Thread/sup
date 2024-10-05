from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .user import User

    # from .workspace import Workspace
    # from .category import Category


class Meet(Base, IntIdPkMixin, DatetimeFieldsMixin):
    name: Mapped[str]
    meet_at: Mapped[datetime]
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspace.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    assigned_to: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

    participants: Mapped[list['Participant']] = relationship(back_populates='meet')

    owner: Mapped['User'] = relationship(
        'User', foreign_keys=[owner_id], back_populates='owned_meetings'
    )

    assigned: Mapped['User'] = relationship(
        'User', foreign_keys=[assigned_to], back_populates='assigned_meetings'
    )


class Participant(Base, IntIdPkMixin, DatetimeFieldsMixin):
    meet_id: Mapped[int] = mapped_column(ForeignKey('meet.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str]

    user: Mapped['User'] = relationship('User', back_populates='participations')
    meet: Mapped['Meet'] = relationship('Meet', back_populates='participant')

    __table_args__ = (UniqueConstraint('meet_id', 'user_id'),)
