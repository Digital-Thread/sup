from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.feature import Priority, Status
from data_access.models import Base

# пока нет по указанным путям
if TYPE_CHECKING:
    from .project import ProjectModel
    from .tag import TagModel
    from .user import UserModel
    from .workspace import WorkspaceModel

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

    owner: Mapped['UserModel'] = relationship(back_populates='owned_features')

    assigned_to: Mapped['UserModel'] = relationship(back_populates='assigned_features')

    tags: Mapped[list['TagModel'] | None] = relationship(
        secondary=feature_tag,
        back_populates='features',
        passive_deletes=True,
    )

    members: Mapped[list['UserModel'] | None] = relationship(
        secondary=feature_member,
        back_populates='features',
        passive_deletes=True,
    )
