from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID


@dataclass
class CreateTagAppDTO:
    name: str
    color: str
    workspace_id: UUID


@dataclass
class TagAppDTO:
    id: int
    name: str
    color: str
    workspace_id: UUID


@dataclass
class UpdateTagAppDTO:
    name: str | None = None
    color: str | None = None
