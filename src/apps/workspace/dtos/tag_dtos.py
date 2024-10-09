from typing import TypedDict
from uuid import UUID

from .base_dto import BaseDTO


class CreateTagAppDTO(TypedDict):
    name: str
    color: str
    workspace_id: UUID


class TagAppDTO(BaseDTO):
    id: int
    name: str
    color: str


class UpdateTagAppDTO(TypedDict, total=False):
    name: str
    color: str
