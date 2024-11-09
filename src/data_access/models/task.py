from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Index, Integer, String, Table
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.task.domain import Priority, Status
from src.data_access.models import Base

if TYPE_CHECKING:
    from .feature import FeatureModel
    from .user import UserModel
    from .workspace_models.tag import TagModel
    from .workspace_models.workspace import WorkspaceModel

task_tag = Table(
    'task_tag',
    Base.metadata,
    Column('task_id', ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
)


class TaskModel(Base):
    __tablename__ = 'tasks'

    __table_args__ = (
        Index('ix_tasks_feature_id', 'feature_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    due_date: Mapped[date] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(String(10_000))
    priority: Mapped[Priority] = mapped_column(Integer)
    status: Mapped[Status] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    workspace_id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey('workspaces.id'),
    )

    feature_id: Mapped[int] = mapped_column(ForeignKey('features.id', ondelete='CASCADE'))

    owner_id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), ForeignKey('users.id'))

    assigned_to_id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True), ForeignKey('users.id')
    )

    workspace: Mapped['WorkspaceModel'] = relationship(
        back_populates='tasks',
    )

    feature: Mapped['FeatureModel'] = relationship(
        back_populates='tasks',
    )

    owner: Mapped['UserModel'] = relationship(
        back_populates='owned_tasks', foreign_keys=[owner_id]
    )

    assigned_to: Mapped['UserModel'] = relationship(
        back_populates='assigned_tasks', foreign_keys=[assigned_to_id]
    )

    tags: Mapped[list['TagModel'] | None] = relationship(
        secondary=task_tag,
        back_populates='tasks',
        passive_deletes=True,
    )
