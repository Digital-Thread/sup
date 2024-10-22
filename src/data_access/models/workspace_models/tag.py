from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.data_access.models.base import Base
from src.data_access.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from src.data_access.models.stubs import FeatureModel
    from src.data_access.models.workspace_models.workspace import WorkspaceModel


class TagModel(Base, IntIdPkMixin):
    __tablename__ = 'tags'

    name: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
    workspace_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('workspaces.id')
    )

    workspace: Mapped['WorkspaceModel'] = relationship(
        'WorkspaceModel', back_populates='tags', cascade='all, delete-orphan'
    )
    features: Mapped[list['FeatureModel']] = relationship('FeatureModel', back_populates='tag')