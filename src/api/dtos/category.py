from pydantic import BaseModel, ConfigDict, Field


class CategoryResponseDTO(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
