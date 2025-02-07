from dataclasses import dataclass
from uuid import UUID

from src.apps.workspace.dtos.pagination_dto import PaginationDTO


@dataclass
class CreateTagDTO:
    name: str
    color: str
    workspace_id: UUID


@dataclass
class TagOutDTO:
    id: int
    name: str
    color: str


@dataclass
class GetTagsDTO(PaginationDTO):
    workspace_id: UUID


@dataclass
class UpdateTagAppDTO:
    id: int
    workspace_id: UUID
    name: str | None = None
    color: str | None = None
