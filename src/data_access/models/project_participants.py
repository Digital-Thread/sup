from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .project import ProjectModel


class ProjectParticipantsModel(Base, IntIdPkMixin):
    __tablename__ = 'project_participants'

    participant_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')
    )
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE')
    )
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))

    project: Mapped['ProjectModel'] = relationship('ProjectModel', back_populates='participants')

    __table_args__ = (
        UniqueConstraint(
            'project_id',
            'workspace_id',
            'participant_id',
            name='uix_workspace_project_participants',
        ),
    )
