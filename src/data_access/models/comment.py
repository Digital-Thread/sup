from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin
from .user import UserModel


class CommentModel(Base, IntIdPkMixin):
    __tablename__ = 'comments'

    user_id: Mapped['UserModel'] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    task_id: Mapped[int] = mapped_column(nullable=True)
    feature_id: Mapped[int] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    user: Mapped['UserModel'] = relationship(back_populates='comments', foreign_keys=[user_id])
