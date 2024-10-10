from enum import Enum

from src.apps.meet.dtos import ParticipantResponseDTO

from .value_objects import MeetId, ParticipantId, UserId


class Status(str, Enum):
    UNDEFINED = 'undefined'
    PRESENT = 'present'
    ABSENT = 'absent'
    WARNED = 'warned'

    @property
    def display(self) -> str:
        return self.name


class Participant:
    def __init__(
        self,
        user_id: UserId,
        status: Status = Status.UNDEFINED,
    ):
        self.user_id = user_id
        self.status = status
        self._id: ParticipantId | None = None
        self._meet_id: MeetId | None = None

    @property
    def id(self) -> ParticipantId:
        if self._id is None:
            raise ValueError('Participant id is None.')
        return self._id

    @id.setter
    def id(self, value: ParticipantId) -> None:
        self._id = value

    @property
    def meet_id(self) -> MeetId:
        if self._meet_id is None:
            raise ValueError('Meet id is None.')
        return self._meet_id

    @meet_id.setter
    def meet_id(self, value: MeetId) -> None:
        self._meet_id = value

    def to_dto(self) -> ParticipantResponseDTO:
        return ParticipantResponseDTO(
            id=self.id,
            user_id=self.user_id,
            meet_id=self.meet_id,
            status=self.status.display,
        )
