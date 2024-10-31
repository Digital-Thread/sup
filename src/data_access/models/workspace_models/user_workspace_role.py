from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_access.models import Base
from src.data_access.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from src.data_access.models.stubs import UserModel
    from src.data_access.models.workspace_models.role import RoleModel


class UserWorkspaceRoleModel(Base, IntIdPkMixin):
    __tablename__ = 'user_workspace_roles'

    user_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')
    )
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE')
    )
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete='CASCADE'))

    user: Mapped['UserModel'] = relationship('UserModel', back_populates='workspaces_roles')
    role: Mapped['RoleModel'] = relationship('RoleModel', back_populates='users')
