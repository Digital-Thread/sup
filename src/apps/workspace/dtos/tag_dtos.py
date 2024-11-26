from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseTagDTO:
    id: int
    workspace_id: UUID


@dataclass
class CreateTagAppDTO:
    name: str
    color: str
    workspace_id: UUID
    
    
@dataclass
class TagOutDTO(BaseTagDTO):
    name: str
    color: str


@dataclass
class GetTagsAppDTO:
    workspace_id: UUID


@dataclass
class UpdateTagAppDTO(BaseTagDTO):
    name: str | None = None
    color: str | None = None


class DeleteTagAppDTO(BaseTagDTO):
    pass
