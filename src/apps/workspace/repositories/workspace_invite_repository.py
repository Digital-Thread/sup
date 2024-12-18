from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInviteEntity
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IWorkspaceInviteRepository(IBaseRepository[WorkspaceInviteEntity, InviteId]):
    @abstractmethod
    async def get_by_workspace_id(self) -> list[WorkspaceInviteEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_code(self, code: UUID) -> tuple[WorkspaceId, InviteId]:
        raise NotImplementedError
