from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_access.models import Base

if TYPE_CHECKING:
    from . import TaskModel
    from .project import ProjectModel
    from .user import UserModel
    from .workspace_models.tag import TagModel
    from .workspace_models.workspace import WorkspaceModel

feature_tag = Table(
    'feature_tag',
    Base.metadata,
    Column('feature_id', ForeignKey('features.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
)

feature_member = Table(
    'feature_user',
    Base.metadata,
    Column('feature_id', ForeignKey('features.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
)


class Priority(IntEnum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NO_PRIORITY = 1


class Status(IntEnum):
    FINISH = 4
    TEST = 3
    DEVELOPMENT = 2
    NEW = 1


class FeatureModel(Base):
    __tablename__ = 'features'

    __table_args__ = (
        Index('ix_features_workspace_id', 'workspace_id'),
        Index('ix_features_project_id', 'project_id'),
        Index('ix_features_assigned_to_id', 'assigned_to_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(10_000))
    priority: Mapped[Priority] = mapped_column(Integer)
    status: Mapped[Status] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    workspace_id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey('workspaces.id'),
    )

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))

    owner_id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), ForeignKey('users.id'))

    assigned_to_id: Mapped[UUID | None] = mapped_column(
        SQL_UUID(as_uuid=True), ForeignKey('users.id')
    )

    workspace: Mapped['WorkspaceModel'] = relationship(
        back_populates='features',
    )

    project: Mapped['ProjectModel'] = relationship(
        back_populates='features',
    )

    owner: Mapped['UserModel'] = relationship(
        back_populates='owned_features', foreign_keys=[owner_id]
    )

    assigned_to: Mapped['UserModel'] = relationship(
        back_populates='assigned_features', foreign_keys=[assigned_to_id]
    )

    tags: Mapped[list['TagModel'] | None] = relationship(
        secondary=feature_tag,
        back_populates='features',
        passive_deletes=True,
    )

    members: Mapped[list['UserModel'] | None] = relationship(
        secondary=feature_member,
        back_populates='member_features',
        passive_deletes=True,
    )

    tasks: Mapped[list['TaskModel']] = relationship('TaskModel', back_populates='feature')
