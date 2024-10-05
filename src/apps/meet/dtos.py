from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, TypedDict
from uuid import UUID


@dataclass
class MeetInputDTO:
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[int]


class OptionalUpdateMeetFields(TypedDict, total=False):
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: int
    participants: list[int]


@dataclass
class MeetUpdateDTO:
    id: int
    updated_fields: OptionalUpdateMeetFields


@dataclass
class MeetResponseDTO(MeetInputDTO):
    id: int
    owner_id: UUID


@dataclass
class InvitedMeetDTO(MeetInputDTO):
    meet_id: int
    user_id: UUID
    status: str


@dataclass
class ParticipantUpdateDTO:
    id: int
    status: str


@dataclass
class ParticipantResponseDTO:
    id: int
    user_id: UUID
    meet_id: int
    status: str


class OrderByField(Enum):
    NAME = 'name'
    ASSIGNED_TO = 'assigned_to'
    CREATED_AT = 'created_at'
    MEET_AT = 'meet_at'


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SortBy(NamedTuple):
    field: OrderByField
    order: SortOrder


class MeetFilterFields(TypedDict, total=False):
    category: int
    assigned_to: UUID
    meet_at: datetime


@dataclass
class MeetListQueryDTO:
    filters: MeetFilterFields | None = None
    order_by: SortBy = SortBy(OrderByField.MEET_AT, SortOrder.DESC)
    limit: Literal[5, 10] = 10
    offset: int = 0
