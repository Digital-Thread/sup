from pydantic import BaseModel


class PermissionResponseDTO(BaseModel):
    id: int
    description: str
