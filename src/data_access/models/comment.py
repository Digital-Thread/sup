from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin
from .user import User


class CommentModel(Base, IntIdPkMixin, DatetimeFieldsMixin):
    __tablename__ = 'comments'  # type: ignore

    user_id: Mapped['User'] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    task_id: Mapped[int] = mapped_column(nullable=True)
    feature_id: Mapped[int] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
