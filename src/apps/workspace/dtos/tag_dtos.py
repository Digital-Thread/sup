from dataclasses import dataclass
from uuid import UUID



@dataclass
class CreateTagDTO:
    name: str
    color: str
    workspace_id: UUID

    
@dataclass
class TagOutDTO:
    id: int
    name: str
    color: str


@dataclass
class UpdateTagAppDTO:
    id: int
    workspace_id: UUID
    name: str | None = None
    color: str | None = None
