from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_access.models.base import Base
from src.data_access.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from src.data_access.models.feature import FeatureModel
    from src.data_access.models.task import TaskModel
    from src.data_access.models.workspace_models.workspace import WorkspaceModel


class TagModel(Base, IntIdPkMixin):
    __tablename__ = 'tags'

    name: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE')
    )

    workspace: Mapped['WorkspaceModel'] = relationship('WorkspaceModel', back_populates='tags')
    features: Mapped[list['FeatureModel']] = relationship(
        'FeatureModel', secondary='feature_tag', back_populates='tags'
    )
    tasks: Mapped[list['TaskModel']] = relationship(
        'TaskModel', secondary='task_tag', back_populates='tags'
    )

    __table_args__ = (UniqueConstraint('name', 'workspace_id', name='uix_name_workspace_id_tags'),)
