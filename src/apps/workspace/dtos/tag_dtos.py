from dataclasses import dataclass
from uuid import UUID



@dataclass
class CreateTagAppDTO:
    name: str
    color: str

    
@dataclass
class TagOutDTO:
    id: int
    name: str
    color: str
    workspace_id: UUID


@dataclass
class UpdateTagAppDTO:
    id: int
    name: str | None = None
    color: str | None = None
