from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UUIDPkMixin
from .project import ProjectModel


class UserModel(Base, UUIDPkMixin):
    __tablename__ = 'users'

    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)

    owned_workspaces: Mapped[list['WorkspaceModel']] = relationship(
        'WorkspaceModel', back_populates='owner', cascade='all, delete-orphan'
    )


class WorkspaceModel(Base, UUIDPkMixin):
    __tablename__ = 'workspaces'

    owner_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')
    )
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None]
    logo: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    owner: Mapped['UserModel'] = relationship('UserModel', back_populates='owned_workspaces')

    projects: Mapped[list['ProjectModel']] = relationship(
        'ProjectModel', back_populates='workspace', cascade='all, delete-orphan'
    )
