from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from src.data_access.models.feature import FeatureModel
    from src.data_access.models.workspace_models.workspace import WorkspaceModel


class ProjectModel(Base, IntIdPkMixin):
    __tablename__ = 'projects'

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None]
    logo: Mapped[str | None]
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    assigned_to: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), ForeignKey('users.id'))
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE')
    )
    owner_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), ForeignKey('users.id'))

    features: Mapped[list['FeatureModel']] = relationship(
        'FeatureModel', back_populates='project', cascade='all, delete-orphan'
    )
    workspace: Mapped['WorkspaceModel'] = relationship('WorkspaceModel', back_populates='projects')

    __table_args__ = (
        UniqueConstraint('name', 'workspace_id', name='uix_name_workspace_id_projects'),
    )
