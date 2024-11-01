from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.apps.project.domain.entity.project import StatusProject


class CreateProjectDTO(BaseModel):
    workspace_id: UUID
    owner_id: UUID
    name: str
    logo: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: StatusProject = Field(default=StatusProject.DISCUSSION)
    assigned_to: UUID | None = Field(default=None)
    participant_ids: list[UUID] | None = Field(default=None)


class ResponseProjectDTO(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)


class UpdateProjectDTO(BaseModel):
    name: str | None = Field(default=None)
    logo: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: StatusProject | None = Field(default=None)
    assigned_to: UUID | None = Field(default=None)
    participant_ids: list[UUID] | None = Field(default=None)
