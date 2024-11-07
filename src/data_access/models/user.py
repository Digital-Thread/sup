from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, UUIDPkMixin

if TYPE_CHECKING:
    from .feature import FeatureModel
    from .workspace_models.user_workspace_role import UserWorkspaceRoleModel
    from .workspace_models.workspace import WorkspaceModel


class UserModel(Base, DatetimeFieldsMixin, UUIDPkMixin):
    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    username_tg: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_tg: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_gmeet: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_gitlab: Mapped[str] = mapped_column(String(50), nullable=True)
    nick_github: Mapped[str] = mapped_column(String(50), nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    owned_workspaces: Mapped[list['WorkspaceModel']] = relationship(
        'WorkspaceModel', back_populates='owner', cascade='all, delete-orphan'
    )
    workspaces: Mapped[list['WorkspaceModel']] = relationship(
        'WorkspaceModel', secondary='workspace_members', back_populates='members'
    )
    workspaces_roles: Mapped[list['UserWorkspaceRoleModel']] = relationship(
        'UserWorkspaceRoleModel', back_populates='user', cascade='all, delete-orphan'
    )

    owned_features: Mapped[list['FeatureModel']] = relationship(
        'FeatureModel', back_populates='owner', foreign_keys='FeatureModel.owner_id'
    )
    member_features: Mapped[list['FeatureModel']] = relationship(
        'FeatureModel', secondary='feature_user', back_populates='members'
    )
    assigned_features: Mapped[list['FeatureModel']] = relationship(
        'FeatureModel', back_populates='assigned_to', foreign_keys='FeatureModel.assigned_to_id'
    )
