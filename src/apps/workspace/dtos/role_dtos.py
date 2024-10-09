from typing import TypedDict
from uuid import UUID

from .base_dto import BaseDTO


class CreatRoleAppDTO(TypedDict):
    name: str
    color: str
    workspace_id: UUID


class RoleAppDTO(BaseDTO):
    id: int
    name: str
    color: str


class UpdateRoleAppDTO(TypedDict, total=False):
    name: str
    color: str
