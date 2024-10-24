from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_access.models.base import Base
from src.data_access.models.mixins import UUIDPkMixin

if TYPE_CHECKING:
    from src.data_access.models.stubs import MeetModel, ProjectModel, UserModel
    from src.data_access.models.workspace_models.category import CategoryModel
    from src.data_access.models.workspace_models.role import RoleModel
    from src.data_access.models.workspace_models.tag import TagModel
    from src.data_access.models.workspace_models.workspace_invite import (
        WorkspaceInviteModel,
    )


class WorkspaceModel(Base, UUIDPkMixin):
    __tablename__ = 'workspaces'

    owner_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')
    )
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[Optional[str]]
    logo: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    owner: Mapped['UserModel'] = relationship(
        'UserModel', back_populates='owned_workspaces', cascade='all, delete-orphan'
    )
    members: Mapped[list['UserModel']] = relationship(
        'UserModel', secondary='workspace_members', back_populates='workspaces'
    )
    projects: Mapped[list['ProjectModel']] = relationship(
        'ProjectModel', back_populates='workspace', cascade='all, delete-orphan'
    )
    meets: Mapped[list['MeetModel']] = relationship(
        'MeetModel', back_populates='workspace', cascade='all, delete-orphan'
    )
    roles: Mapped[list['RoleModel']] = relationship(
        'RoleModel', back_populates='workspace', cascade='all, delete-orphan'
    )
    tags: Mapped[list['TagModel']] = relationship(
        'TagModel', back_populates='workspace', cascade='all, delete-orphan'
    )
    categories: Mapped[list['CategoryModel']] = relationship(
        'CategoryModel', back_populates='workspace', cascade='all, delete-orphan'
    )
    invites: Mapped[list['WorkspaceInviteModel']] = relationship(
        'WorkspaceInviteModel', back_populates='workspace', cascade='all, delete-orphan'
    )
