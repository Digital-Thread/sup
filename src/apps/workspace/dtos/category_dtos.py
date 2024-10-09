from typing import TypedDict
from uuid import UUID

from .base_dto import BaseDTO


class CreateCategoryAppDTO(TypedDict):
    name: str
    workspace_ids: set[UUID]


class CategoryAppDTO(BaseDTO):
    id: int
    name: str
    workspace_ids: set[UUID]


class UpdateCategoryAppDTO(TypedDict, total=False):
    name: str
    workspace_ids: set[UUID]
