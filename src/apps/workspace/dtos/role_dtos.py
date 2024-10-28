from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID


class CreateRoleAppDTO(TypedDict):
    name: str
    color: str
    workspace_id: UUID


@dataclass
class RoleWithUserCountAppDTO:
    id: int
    name: str
    color: str
    user_count: int


class UpdateRoleAppDTO(TypedDict, total=False):
    name: str
    color: str
