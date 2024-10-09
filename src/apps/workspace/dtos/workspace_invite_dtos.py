from datetime import datetime
from typing import TypedDict
from uuid import UUID

from src.apps.workspace.dtos.base_dto import BaseDTO


class CreateWorkspaceInviteAppDTO(TypedDict):
    workspace_id: UUID
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


class WorkspaceInviteAppDTO(BaseDTO):
    id: int
    workspace_id: UUID
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


class UpdateWorkspaceInviteAppDTO(TypedDict):
    status: str
