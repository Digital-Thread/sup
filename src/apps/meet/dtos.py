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
