from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateCategoryAppDTO:
    name: str
    workspace_id: UUID


@dataclass
class CategoryOutDTO:
    id: int
    workspace_id: UUID
    name: str


@dataclass
class UpdateCategoryAppDTO:
    category_id: int
    name: str | None = None
