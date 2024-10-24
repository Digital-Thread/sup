"""Заглушка, удалю перед слиянием с остальными ветками!"""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin, UUIDPkMixin

if TYPE_CHECKING:
    from src.data_access.models.workspace_models.category import CategoryModel
    from src.data_access.models.workspace_models.tag import TagModel
    from src.data_access.models.workspace_models.user_workspace_role import (
        UserWorkspaceRoleModel,
    )
    from src.data_access.models.workspace_models.workspace import WorkspaceModel


class UserModel(Base, UUIDPkMixin):
    __tablename__ = 'users'

    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)

    owned_workspaces: Mapped[list['WorkspaceModel']] = relationship(
        'WorkspaceModel', back_populates='owner', cascade='all, delete-orphan'
    )
    workspaces: Mapped[list['WorkspaceModel']] = relationship(
        'WorkspaceModel', secondary='workspace_members', back_populates='members'
    )
    workspaces_roles: Mapped[list['UserWorkspaceRoleModel']] = relationship(
        'UserWorkspaceRoleModel', back_populates='user', cascade='all, delete-orphan'
    )


class MeetModel(Base, IntIdPkMixin, DatetimeFieldsMixin):
    __tablename__ = 'meets'

    name: Mapped[str]
    meet_at: Mapped[datetime]
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE')
    )
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    workspace: Mapped['WorkspaceModel'] = relationship('WorkspaceModel', back_populates='meets')
    category: Mapped['CategoryModel'] = relationship('CategoryModel', back_populates='meets')


class FeatureModel(Base, IntIdPkMixin):
    __tablename__ = 'features'

    name: Mapped[str]
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'))

    tag: Mapped['TagModel'] = relationship('TagModel', back_populates='features')
    project: Mapped['ProjectModel'] = relationship('ProjectModel', back_populates='features')


class ProjectModel(Base, IntIdPkMixin):
    __tablename__ = 'projects'

    name: Mapped[str]
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE')
    )

    features: Mapped[list['FeatureModel']] = relationship('FeatureModel', back_populates='project')
    workspace: Mapped['WorkspaceModel'] = relationship('WorkspaceModel', back_populates='projects')
