from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateWorkspaceDTO(BaseModel):
    name: str
    owner_id: UUID


class ResponseWorkspaceDTO(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    created_at: datetime
    description: str | None = Field(exclude=True)
    logo: str | None = Field(exclude=True)
    invite_ids: list[int] = Field(exclude=True)
    project_ids: list[int] = Field(exclude=True)
    meet_ids: list[int] = Field(exclude=True)
    tag_ids: list[int] = Field(exclude=True)
    role_ids: list[int] = Field(exclude=True)
    member_ids: list[UUID] = Field(exclude=True)

    model_config = ConfigDict(from_attributes=True)


class UpdateWorkspaceDTO(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    logo: str | None = Field(default=None)
