from datetime import datetime, timezone
from enum import Enum
from typing import Literal, TypedDict

from .type_ids import MeetId, ParticipantId, UserId


class Status(Enum):
    UNDEFINED = 'undefined'
    PRESENT = 'present'
    ABSENT = 'absent'
    WARNED = 'warned'

    @classmethod
    def from_display(cls, display: str) -> 'Status':
        try:
            return cls(display)
        except ValueError as e:
            raise ValueError(f'Invalid display value: {display}') from e

    @property
    def display(self) -> Literal['undefined', 'present', 'absent', 'warned']:
        return self.value


class OptionalParticipantUpdateFields(TypedDict, total=False):
    status: Status


class ParticipantEntity:
    def __init__(
        self,
        user_id: UserId,
        status: Status = Status.UNDEFINED,
    ):
        self.user_id = user_id
        self.status = status
        self._id: ParticipantId | None = None
        self._meet_id: MeetId | None = None
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    @property
    def id(self) -> ParticipantId:
        if self._id is None:
            raise AttributeError('Participant id is not set.')
        return self._id

    @id.setter
    def id(self, _id: ParticipantId) -> None:
        if self._id is None:
            raise AttributeError('Participant id is already set.')
        self._id = _id

    @property
    def meet_id(self) -> MeetId:
        if self._meet_id is None:
            raise AttributeError('Meet id is not set.')
        return self._meet_id

    @meet_id.setter
    def meet_id(self, _id: MeetId) -> None:
        if self._meet_id is None:
            raise AttributeError('Meet id is already set.')
        self._meet_id = _id

    def update_fields(self, updates: OptionalParticipantUpdateFields) -> None:
        for field, value in updates.items():
            setattr(self, field, value)
        self.updated_at = datetime.now(timezone.utc)
