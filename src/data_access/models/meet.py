from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .user import UserModel
    from .workspace_models.category import CategoryModel
    from .workspace_models.workspace import WorkspaceModel


class MeetModel(Base, IntIdPkMixin, DatetimeFieldsMixin):
    __tablename__ = 'meets'

    name: Mapped[str]
    meet_at: Mapped[datetime]
    workspace_id: Mapped[UUID] = mapped_column(ForeignKey('workspaces.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    assigned_to: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

    participants: Mapped[list['ParticipantModel']] = relationship(
        cascade='all, delete-orphan', back_populates='meet', lazy='raise_on_sql'
    )

    owner: Mapped['UserModel'] = relationship(
        'UserModel', foreign_keys=[owner_id], back_populates='owned_meetings'
    )

    assigned: Mapped['UserModel'] = relationship(
        'UserModel', foreign_keys=[assigned_to], back_populates='assigned_meetings'
    )

    workspace: Mapped['WorkspaceModel'] = relationship(
        'WorkspaceModel', foreign_keys=[workspace_id], back_populates='meets', lazy='raise_on_sql'
    )

    category: Mapped['CategoryModel'] = relationship(
        'CategoryModel', back_populates='meets', lazy='joined'
    )


class ParticipantModel(Base, IntIdPkMixin, DatetimeFieldsMixin):
    __tablename__ = 'participants'

    meet_id: Mapped[int] = mapped_column(ForeignKey('meets.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str]

    user: Mapped['UserModel'] = relationship(
        'UserModel', back_populates='participations', lazy='joined'
    )
    meet: Mapped['MeetModel'] = relationship(
        'MeetModel', back_populates='participants', lazy='raise_on_sql'
    )

    __table_args__ = (UniqueConstraint('meet_id', 'user_id'),)
