from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateCategoryDTO(BaseModel):
    name: str
    workspace_id: UUID


class ResponseCategoryDTO(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UpdateCategoryDTO(BaseModel):
    name: str | None = Field(default=None)
