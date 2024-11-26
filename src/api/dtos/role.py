from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateRoleDTO(BaseModel):
    name: str
    color: str
    workspace_id: UUID


class RoleWithUserCountResponseDTO(BaseModel):
    id: int
    name: str
    color: str
    user_count: int

    model_config = ConfigDict(from_attributes=True)


class RoleResponseDTO(BaseModel):
    id: int
    name: str
    color: str


class UpdateRoleDTO(BaseModel):
    name: str | None = Field(default=None)
    color: str | None = Field(default=None)
