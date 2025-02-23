from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UUID as SQL_UUID
from sqlalchemy import Enum, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.meet.domain import Status
from src.data_access.models import Base

from .mixins import DatetimeFieldsMixin, IntIdPkMixin

if TYPE_CHECKING:
    from .meet import MeetModel
    from .user import UserModel


class ParticipantModel(Base, DatetimeFieldsMixin, IntIdPkMixin):
    __tablename__ = 'meet_participants'

    __table_args__ = (
        Index('ix_meet_participant_user_id', 'user_id'),
        UniqueConstraint('meet_id', 'user_id'),
    )

    meet_id: Mapped[int] = mapped_column(ForeignKey('meets.id'))
    user_id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), ForeignKey('users.id'))
    status: Mapped[Status] = mapped_column(Enum(Status))

    user: Mapped['UserModel'] = relationship(
        'UserModel', back_populates='meet_participants', foreign_keys=[user_id], lazy='joined'
    )

    meet: Mapped['MeetModel'] = relationship(
        'MeetModel', back_populates='participants', lazy='raise_on_sql'
    )
