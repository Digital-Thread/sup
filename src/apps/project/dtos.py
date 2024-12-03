from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.project.domain.project import StatusProject


@dataclass
class ProjectCreateDTO:
    owner_id: UUID
    name: str
    status: StatusProject
    logo: str | None = None
    description: str | None = None
    assigned_to: UUID | None = None
    participant_ids: list[UUID] | None = None


@dataclass
class ProjectWithParticipantCountDTO:
    id: int
    workspace_id: UUID
    owner_id: UUID
    name: str
    logo: str | None
    description: str | None
    status: StatusProject
    created_at: datetime | None
    assigned_to: UUID | None
    participants_count: int


@dataclass
class ProjectUpdateDTO:
    name: str | None = None
    logo: str | None = None
    description: str | None = None
    status: StatusProject | None = None
    assigned_to: UUID | None = None
    participant_ids: list[UUID] | None = None


@dataclass
class ProjectWithParticipantsDTO:
    id: int
    workspace_id: UUID
    owner_id: UUID
    name: str
    logo: str | None
    description: str | None
    status: StatusProject
    created_at: datetime | None
    assigned_to: UUID | None
    participants: list[dict[str, UUID | str | bool]]
