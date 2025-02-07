from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import DatetimeFieldsMixin, IntIdPkMixin
from .user import UserModel


class CommentModel(Base, IntIdPkMixin, DatetimeFieldsMixin):
    __tablename__ = 'comments'

    user_id: Mapped['UserModel'] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    task_id: Mapped[int] = mapped_column(nullable=True)
    feature_id: Mapped[int] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
