from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseCategoryDTO:
    id: int
    workspace_id: UUID


@dataclass
class CreateCategoryAppDTO:
    name: str
    workspace_id: UUID


@dataclass
class CategoryOutDTO(BaseCategoryDTO):
    name: str


@dataclass
class GetCategoriesAppDTO:
    workspace_id: UUID


@dataclass
class UpdateCategoryAppDTO(BaseCategoryDTO):
    name: str | None = None


@dataclass
class DeleteCategoryAppDTO(BaseCategoryDTO):
    pass