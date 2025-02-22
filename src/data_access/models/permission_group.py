from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Table, Boolean, ForeignKey, String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID as SQL_UUID

from src.data_access.models import Base

if TYPE_CHECKING:
    from .permission import PermissionModel
    from .user import UserModel

permission_group_permissions = Table(
    'permission_group_permissions',
    Base.metadata,
    Column('permission_group_id', ForeignKey('permission_groups.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

permission_group_users = Table(
    'permission_group_users',
    Base.metadata,
    Column('permission_group_id', ForeignKey('permission_groups.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('workspace_id', ForeignKey('workspaces.id'), nullable=True)
)


class PermissionGroupModel(Base):
    __tablename__ = 'permission_groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    is_global: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    workspace_id: Mapped[UUID | None] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey('workspaces.id'),
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    permissions: Mapped[set['PermissionModel']] = relationship(
        secondary=permission_group_permissions,
        back_populates='permission_groups',
        collection_class=set
    )
    authorized_users: Mapped[set['UserModel']] = relationship(
        secondary=permission_group_users,
        back_populates='permission_groups',
        collection_class=set,
    )
