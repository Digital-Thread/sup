from data_access.models.meet import Meet, Participant
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import DatetimeFieldsMixin, UUIDPkMixin


class User(Base, DatetimeFieldsMixin, UUIDPkMixin):
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)

    owned_meetings: Mapped[list['Meet']] = relationship(
        'Meet', foreign_keys='Meet.owner_id', back_populates='owner'
    )
    assigned_meetings: Mapped[list['Meet']] = relationship(
        'Meet', foreign_keys='Meet.assigned_to', back_populates='assigned'
    )
    participations: Mapped[list['Participant']] = relationship('Participant', back_populates='user')
