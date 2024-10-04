from enum import IntEnum

from .value_objects import MeetId, ParticipantId


class Status(IntEnum):
    UNDEFINED = 1
    PRESENT = 2
    ABSENT = 3
    WARNED = 4

    @property
    def display(self) -> str:
        return self.name


class Participant:
    def __init__(
        self,
        user_id: ParticipantId,
        meet_id: MeetId,
        status: Status = Status.UNDEFINED,
    ):
        self.user_id = user_id
        self.meet_id = meet_id
        self.status = status
        self._id: ParticipantId | None = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: ParticipantId):
        self._id = value
