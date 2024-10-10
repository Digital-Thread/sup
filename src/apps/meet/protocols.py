from typing import Protocol
from uuid import UUID


class WorkspaceServiceProtocol(Protocol):
    async def user_has_access(self, user_id: UUID, workspace_id: int) -> bool:
        """Check if user has access to the workspace"""
        ...


class WorkspaceService:
    async def user_has_access(self, user_id: UUID, workspace_id: int) -> bool:
        return True
