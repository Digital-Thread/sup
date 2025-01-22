from datetime import datetime, timezone
from re import match
from typing import TypedDict

from .participant import ParticipantEntity
from .type_ids import AssignedId, CategoryId, MeetId, OwnerId, WorkspaceId


class OptionalMeetUpdateFields(TypedDict, total=False):
    name: str
    meet_at: datetime
    category_id: CategoryId
    assigned_to: AssignedId
    participants: list[ParticipantEntity]


class MeetEntity:
    _NAME_MAX_LENGHT = 50

    def __init__(
        self,
        workspace_id: WorkspaceId,
        name: str,
        meet_at: datetime,
        category_id: CategoryId,
        owner_id: OwnerId,
        assigned_to: AssignedId,
        participants: list[ParticipantEntity],
    ):
        self._id: MeetId | None = None
        self.workspace_id = workspace_id
        self.name = name
        self.meet_at = meet_at
        self.category_id = category_id
        self.owner_id = owner_id
        self.assigned_to = assigned_to
        self.participants = participants if participants else []
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    @property
    def id(self) -> MeetId:
        if self._id is None:
            raise AttributeError('Meet id is not set.')
        return self._id

    @id.setter
    def id(self, _id: MeetId) -> None:
        if self._id is not None:
            raise AttributeError('Meet id is already set.')

        self._id = _id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._validate_name(value)
        self._name = value

    def _validate_name(self, name: str) -> None:
        pattern = r'^[a-zA-Zа-яА-ЯёЁ ]+$'
        max_length = self._NAME_MAX_LENGHT
        if not match(pattern, name):
            raise ValueError(
                'Name must consist of letters and spaces, and must not contain special symbols.'
            )
        if len(name) > max_length:
            raise ValueError(f'Name must not be longer than {max_length} characters.')

    @property
    def meet_at(self) -> datetime:
        return self._meet_at

    @meet_at.setter
    def meet_at(self, value: datetime) -> None:
        if value is not None:
            value = value.replace(tzinfo=None)
        self._meet_at = value

    def update_fields(self, updates: OptionalMeetUpdateFields) -> None:
        for field, value in updates.items():
            setattr(self, field, value)
        self.updated_at = datetime.now(timezone.utc)
