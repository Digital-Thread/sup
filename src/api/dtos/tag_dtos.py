from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateTagDTO(BaseModel):
    name: str
    color: str
    workspace_id: UUID


class ResponseTagDTO(BaseModel):
    id: int
    name: str
    color: str

    model_config = ConfigDict(from_attributes=True)


class UpdateTagDTO(BaseModel):
    name: str | None = Field(default=None)
    color: str | None = Field(default=None)
