from dataclasses import dataclass
from uuid import UUID


@dataclass
class CategoryOutDTO:
    id: int
    workspace_id: UUID
    name: str
