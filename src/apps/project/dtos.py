from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.apps.project.domain.project import StatusProject


@dataclass
class ProjectCreateDTO:
    workspace_id: UUID
    owner_id: UUID
    name: str
    status: StatusProject
    logo: str | None = None
    description: str | None = None
    assigned_to: UUID | None = None
    participant_ids: list[UUID] | None = None


@dataclass
class ParticipantOutDTO:
    participant_id: UUID
    first_name: str
    last_name: str
    avatar: str | None


@dataclass
class WorkspaceMemberOutDTO:
    id: UUID
    full_name: str
    is_project_participant: bool


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
    participants: list[ParticipantOutDTO | WorkspaceMemberOutDTO] | None = field(
        default_factory=list
    )


@dataclass
class ProjectUpdateDTO:
    project_id: int
    workspace_id: UUID
    name: str | None = None
    logo: str | None = None
    description: str | None = None
    status: StatusProject | None = None
    assigned_to: UUID | None = None
    participant_ids: list[UUID] | None = None


@dataclass
class PaginationDTO:
    page: int
    page_size: int
