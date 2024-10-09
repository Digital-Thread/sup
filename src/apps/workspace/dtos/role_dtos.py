from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID


class CreatRoleAppDTO(TypedDict):
    name: str
    color: str
    workspace_id: UUID


@dataclass
class RoleAppDTO:
    id: int
    name: str
    color: str
    workspace_id: UUID


class UpdateRoleAppDTO(TypedDict, total=False):
    name: str
    color: str
