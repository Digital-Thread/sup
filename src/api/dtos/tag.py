from pydantic import BaseModel, ConfigDict, Field


class CreateTagRequestDTO(BaseModel):
    name: str
    color: str


class TagResponseDTO(BaseModel):
    id: int
    name: str
    color: str

    model_config = ConfigDict(from_attributes=True)


class UpdateTagDTO(BaseModel):
    name: str | None = Field(default=None)
    color: str | None = Field(default=None)
