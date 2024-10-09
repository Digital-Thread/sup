from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict
from uuid import UUID


class CreateWorkspaceInviteAppDTO(TypedDict):
    workspace_id: UUID
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


@dataclass
class WorkspaceInviteAppDTO:
    id: int
    workspace_id: UUID
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


class UpdateWorkspaceInviteAppDTO(TypedDict):
    status: str
