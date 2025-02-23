from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey, Index, String
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_access.models import Base

from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .meet_participants import ParticipantModel
    from .user import UserModel
    from .workspace_models.category import CategoryModel
    from .workspace_models.workspace import WorkspaceModel


class MeetModel(Base, DatetimeFieldsMixin, IntIdPkMixin):
    __tablename__ = 'meets'

    __table_args__ = (
        Index('ix_meets_workspace_id', 'workspace_id'),
        Index('ix_meets_assigned_to_id', 'assigned_to_id'),
        Index('ix_meets_category_id', 'category_id'),
        Index('ix_meets_owned_id', 'owner_id'),
    )

    name: Mapped[str] = mapped_column(String(50))
    meet_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    workspace_id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), ForeignKey('workspaces.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    owner_id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), ForeignKey('users.id'))
    assigned_to_id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), ForeignKey('users.id'))

    participants: Mapped[list['ParticipantModel']] = relationship(
        cascade='all, delete-orphan', back_populates='meet', lazy='raise_on_sql'
    )

    workspace: Mapped['WorkspaceModel'] = relationship(
        'WorkspaceModel', back_populates='meets', lazy='raise_on_sql', foreign_keys=[workspace_id]
    )
    category: Mapped['CategoryModel'] = relationship(
        'CategoryModel', back_populates='meets', lazy='joined'
    )
    owner: Mapped['UserModel'] = relationship(
        'UserModel', back_populates='owned_meets', foreign_keys=[owner_id], lazy='selectin'
    )
    assigned_to: Mapped['UserModel'] = relationship(
        'UserModel', back_populates='assigned_meets', foreign_keys=[assigned_to_id], lazy='selectin'
    )
