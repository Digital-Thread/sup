from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID


class CreateTagAppDTO(TypedDict):
    name: str
    color: str
    workspace_id: UUID


@dataclass
class TagAppDTO:
    id: int
    name: str
    color: str
    workspace_id: UUID


class UpdateTagAppDTO(TypedDict, total=False):
    name: str
    color: str
