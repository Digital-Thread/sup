from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IWorkspaceInviteRepository(IBaseRepository[WorkspaceInvite, InviteId]):
    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[WorkspaceInvite]:
        raise NotImplementedError
