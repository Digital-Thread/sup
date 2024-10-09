from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID


class CreateCategoryAppDTO(TypedDict):
    name: str
    workspace_id: UUID


@dataclass
class CategoryAppDTO:
    id: int
    name: str
    workspace_id: UUID


class UpdateCategoryAppDTO(TypedDict, total=False):
    name: str
