from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, TypedDict
from uuid import UUID


@dataclass
class ParticipantInputDTO:
    user_id: int
    status: str


@dataclass
class ParticipantResponseDTO:
    id: int
    user_id: UUID
    meet_id: int
    status: str


@dataclass
class MeetInputDTO:
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[ParticipantInputDTO]


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
class MeetResponseDTO:
    id: int
    owner_id: UUID
    name: str
    meet_at: datetime
    category_id: int
    assigned_to: UUID
    participants: list[ParticipantResponseDTO]


@dataclass
class InvitedMeetDTO(MeetInputDTO):
    meet_id: int
    user_id: UUID
    status: str


@dataclass
class ParticipantUpdateDTO:
    id: int
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
    limit: Literal[4, 8, 16, 24] | None = 16
    offset: int = 0
