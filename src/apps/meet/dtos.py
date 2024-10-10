from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, NamedTuple, TypedDict
from uuid import UUID


@dataclass
class ParticipantCreateDTO:
    user_id: UUID
    status: Literal['present', 'absent', 'warned']


@dataclass
class ParticipantUpdateDTO:
    id: int
    status: Literal['present', 'absent', 'warned']


@dataclass
class ParticipantDeleteDTO:
    id: int


@dataclass
class ParticipantResponseDTO:
    id: int
    user_id: UUID
    meet_id: int
    status: Literal['present', 'absent', 'warned']


@dataclass
class MeetCreateDTO:
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[ParticipantCreateDTO]


@dataclass
class MeetUpdateDTO:
    name: str | None = None
    meet_at: datetime | None = None
    category_id: int | None = None
    assigned_to: UUID | None = None
    participants_to_add: list[ParticipantCreateDTO] = field(default_factory=list)
    participants_to_update: list[ParticipantUpdateDTO] = field(default_factory=list)
    participants_to_delete: list[ParticipantDeleteDTO] = field(default_factory=list)


@dataclass
class MeetResponseDTO:
    id: int
    owner_id: UUID
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[ParticipantResponseDTO]


class SortBy(NamedTuple):
    field: Literal['name', 'assigned_to', 'meet_at']
    order: Literal['ASC', 'DESC']


class MeetFilterFields(TypedDict, total=False):
    category_id: int
    assigned_to: UUID
    meet_at: datetime


@dataclass
class MeetListQueryDTO:
    filters: MeetFilterFields | None = None
    order_by: SortBy = SortBy('meet_at', 'DESC')
    limit: Literal[4, 8, 16, 24] | None = 16
    offset: int = 0
