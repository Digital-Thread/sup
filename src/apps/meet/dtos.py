from dataclasses import dataclass
from datetime import datetime

from .domain import (
    AssignedId,
    CategoryId,
    MeetId,
    OptionalMeetUpdateFields,
    OptionalParticipantUpdateFields,
    OwnerId,
    ParticipantId,
    Status,
    UserId,
    WorkspaceId,
)


@dataclass
class ParticipantInputDTO:
    user_id: UserId
    status: Status = Status.UNDEFINED


@dataclass
class MeetInputDTO:
    workspace_id: WorkspaceId
    name: str
    meet_at: datetime
    category_id: CategoryId
    owner_id: OwnerId
    assigned_to: AssignedId
    participants: list[ParticipantInputDTO] | None


@dataclass
class ParticipantOutputDTO:
    id: ParticipantId
    user_id: UserId
    meet_id: MeetId
    status: Status


@dataclass
class MeetOutputDTO:
    id: MeetId
    owner_id: OwnerId
    name: str
    meet_at: datetime
    category_id: CategoryId
    assigned_to: AssignedId
    participants: list[ParticipantOutputDTO] | None


@dataclass
class MeetUpdateDTO:
    id: MeetId
    updated_fields: OptionalMeetUpdateFields


@dataclass
class ParticipantUpdateDTO:
    id: ParticipantId
    updated_fields: OptionalParticipantUpdateFields


# @dataclass
# class ParticipantInputDTO:
#     user_id: UUID
#     status: Literal['present', 'absent', 'warned', 'undefined']


# @dataclass
# class ParticipantUpdateDTO:
#     id: int
#     status: Literal['present', 'absent', 'warned', 'undefined']


# @dataclass
# class ParticipantDeleteDTO:
#     id: int


# @dataclass
# class ParticipantOutputDTO:
#     id: int
#     user_id: UUID
#     meet_id: int
#     status: Literal['present', 'absent', 'warned', 'undefined']


# @dataclass
# class MeetInputDTO:
#     workspace_id: UUID
#     name: str
#     meet_at: datetime
#     category_id: int
#     owner_id: UUID
#     assigned_to: UUID
#     participants: list[ParticipantInputDTO]


# @dataclass
# class MeetUpdateDTO:
#     name: str | None = None
#     meet_at: datetime | None = None
#     category_id: int | None = None
#     assigned_to: UUID | None = None
#     participants_to_add: list[ParticipantInputDTO] = field(default_factory=list)
#     participants_to_update: list[ParticipantUpdateDTO] = field(default_factory=list)
#     participants_to_delete: list[ParticipantDeleteDTO] = field(default_factory=list)


# @dataclass
# class MeetOutputDTO:
#     id: int
#     owner_id: UUID
#     name: str
#     meet_at: datetime
#     category_id: int
#     assigned_to: UUID
#     participants: list[ParticipantOutputDTO]


# class SortBy(NamedTuple):
#     field: Literal['name', 'assigned_to', 'meet_at']
#     order: Literal['ASC', 'DESC']


# class MeetFilterFields(TypedDict, total=False):
#     category_id: int
#     assigned_to: UUID
#     meet_at: datetime


# @dataclass
# class MeetListQueryDTO:
#     filters: MeetFilterFields | None = None
#     order_by: SortBy = SortBy('meet_at', 'DESC')
#     limit: Literal[4, 8, 16, 24] | None = 16
#     offset: int = 0
