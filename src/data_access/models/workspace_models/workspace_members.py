from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data_access.models import Base


class WorkspaceMemberModel(Base):
    __tablename__ = 'workspace_members'

    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey('workspaces.id', ondelete='CASCADE'),
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
    )
