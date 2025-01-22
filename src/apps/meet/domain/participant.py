from datetime import datetime, timezone
from enum import IntEnum
from typing import TypedDict

from .type_ids import MeetId, ParticipantId, UserId


class Status(str, IntEnum):
    UNDEFINED = 0
    PRESENT = 1
    ABSENT = 2
    WARNED = 3

    @property
    def display(self) -> str:
        return {
            self.UNDEFINED: 'undefined',
            self.PRESENT: 'present',
            self.ABSENT: 'absent',
            self.WARNED: 'warned',
        }


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
        self._created_at = datetime.now(timezone.utc)
        self._updated_at = datetime.now(timezone.utc)

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

    # def to_dto(self) -> ParticipantResponseDTO:
    #     return ParticipantResponseDTO(
    #         id=self.id,
    #         user_id=self.user_id,
    #         meet_id=self.meet_id,
    #         status=self.status.display,
    #     )
