from datetime import datetime, timezone
from re import match

from src.apps.meet.dtos import MeetResponseDTO

from .participant import Participant
from .value_objects import AssignedId, CategoryId, MeetId, OwnerId, WorkspaceId


class Meet:
    _NAME_MAX_LENGHT = 50

    def __init__(
        self,
        workspace_id: WorkspaceId,
        name: str,
        meet_at: datetime,
        category_id: CategoryId,
        owner_id: OwnerId,
        assigned_to: AssignedId,
        participants: list[Participant],
    ):
        self._id: MeetId | None = None
        self.workspace_id = workspace_id
        self.name = name
        self.meet_at = meet_at
        self.category_id = category_id
        self.owner_id = owner_id
        self.assigned_to = assigned_to
        self.participants = participants if participants else []
        self._created_at = datetime.now(timezone.utc)
        self._updated_at = datetime.now(timezone.utc)

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

    @property
    def id(self) -> MeetId:
        if self._id is None:
            raise ValueError('Meet id is None.')
        return self._id

    @id.setter
    def id(self, value: MeetId) -> None:
        self._id = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def mark_as_updated(self) -> None:
        self._updated_at = datetime.now(timezone.utc)

    def to_dto(self) -> MeetResponseDTO:
        participants = [p.to_dto() for p in self.participants] if self.participants else []
        return MeetResponseDTO(
            id=self.id,
            name=self.name,
            meet_at=self.meet_at,
            category_id=self.category_id,
            owner_id=self.owner_id,
            assigned_to=self.assigned_to,
            participants=participants,
        )
