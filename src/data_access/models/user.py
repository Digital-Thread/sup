from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, UUIDPkMixin

if TYPE_CHECKING:
    from src.data_access.models.workspace_models.user_workspace_role import (
        UserWorkspaceRoleModel,
    )
    from src.data_access.models.workspace_models.workspace import WorkspaceModel


class UserModel(Base, UUIDPkMixin, DatetimeFieldsMixin):
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
