from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.project.domain.entity.project import StatusProject


@dataclass
class CreateProjectAppDTO:
    workspace_id: UUID
    owner_id: UUID
    name: str
    logo: str | None
    description: str | None
    status: StatusProject
    assigned_to: UUID | None
    feature_ids: list[int] | None
    participant_ids: list[UUID] | None


@dataclass
class ProjectAppDTO:
    id: int
    workspace_id: UUID
    owner_id: UUID
    name: str
    logo: str | None
    description: str | None
    status: StatusProject
    created_at: datetime | None
    assigned_to: UUID | None
    feature_ids: list[int] | None
    participant_ids: list[UUID] | None


@dataclass
class UpdateProjectAppDTO:
    name: str | None = None
    logo: str | None = None
    description: str | None = None
    status: StatusProject | None = None
    assigned_to: list[UUID] | None = None
    feature_ids: list[int] | None = None
    participant_ids: list[UUID] | None = None
