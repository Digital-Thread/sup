from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.apps.project.domain.project import StatusProject


class CreateProjectRequestDTO(BaseModel):
    owner_id: UUID
    name: str
    logo: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: StatusProject = Field(default=StatusProject.DISCUSSION)
    assigned_to: UUID | None = Field(default=None)
    participant_ids: list[UUID] | None = Field(default=None)


class ParticipantResponseDTO(BaseModel):
    participant_id: UUID
    first_name: str
    last_name: str
    avatar: str | None

    model_config = ConfigDict(from_attributes=True)


class WorkspaceMemberResponseDTO(BaseModel):
    id: UUID
    full_name: str
    is_project_participant: bool

    model_config = ConfigDict(from_attributes=True)


class ProjectResponseDTO(BaseModel):
    id: int
    workspace_id: UUID
    owner_id: UUID
    name: str
    logo: str | None
    description: str | None
    status: StatusProject
    created_at: datetime | None
    assigned_to: UUID | None
    participants: list[ParticipantResponseDTO | WorkspaceMemberResponseDTO] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)


class UpdateProjectRequestDTO(BaseModel):
    name: str | None = Field(default=None)
    logo: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: StatusProject | None = Field(default=None)
    assigned_to: UUID | None = Field(default=None)
    participant_ids: list[UUID] | None = Field(default=None)
