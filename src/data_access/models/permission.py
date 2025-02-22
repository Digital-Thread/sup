from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_access.models import Base

if TYPE_CHECKING:
    from .permission_group import PermissionGroupModel


class PermissionModel(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    description: Mapped[str]
    is_hidden: Mapped[bool]

    permission_groups: Mapped[set['PermissionGroupModel']] = relationship(
        'PermissionGroupModel', secondary='permission_group_permissions', back_populates='permissions'
    )
