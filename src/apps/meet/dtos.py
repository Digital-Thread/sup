from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict
from uuid import UUID


@dataclass
class MeetInputDTO:
    workspace_id: int
    name: str
    meet_at: datetime
    category_id: int
    owner_id: UUID
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
