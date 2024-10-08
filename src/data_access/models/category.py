from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .meet import Meet
    from .workspace import Workspace


class Category(Base, IntIdPkMixin, DatetimeFieldsMixin):
    name: Mapped[str]
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspace.id'))

    workspace: Mapped['Workspace'] = relationship(
        'Workspace', back_populates='categories', lazy='raise_on_sql'
    )

    meets: Mapped[list['Meet']] = relationship(
        cascade='all, delete-orphan', back_populates='category', lazy='raise_on_sql'
    )
