from dataclasses import dataclass
from uuid import UUID

from src.apps.workspace.dtos.pagination_dto import PaginationDTO


@dataclass
class CategoryOutDTO:
    id: int
    workspace_id: UUID
    name: str


@dataclass
class GetCategoryDTO(PaginationDTO):
    workspace_id: UUID
