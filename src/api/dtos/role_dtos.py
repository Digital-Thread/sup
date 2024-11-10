from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateRoleDTO(BaseModel):
    name: str
    color: str
    workspace_id: UUID


class ResponseRoleWithUserCountDTO(BaseModel):
    id: int
    name: str
    color: str
    user_count: int

    model_config = ConfigDict(from_attributes=True)


class UpdateRoleDTO(BaseModel):
    name: str | None = Field(default=None)
    color: str | None = Field(default=None)
