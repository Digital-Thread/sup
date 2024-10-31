from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateCategoryAppDTO:
    name: str
    workspace_id: UUID


@dataclass
class CategoryAppDTO:
    id: int
    name: str
    workspace_id: UUID


@dataclass
class UpdateCategoryAppDTO:
    name: str | None = None
