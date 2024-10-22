from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.data_access.models.base import Base
from src.data_access.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from src.data_access.models.workspace_models.workspace import WorkspaceModel


class WorkspaceInviteModel(Base, IntIdPkMixin):
    __tablename__ = 'workspace_invites'

    code: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        default=uuid4,
        server_default=func.uuid_generate_v4(),
        nullable=False,
    )
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    expired_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id')
    )

    workspace: Mapped['WorkspaceModel'] = relationship(
        'WorkspaceModel', back_populates='invites', cascade='all, delete-orphan'
    )
