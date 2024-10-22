from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import OwnerId, RoleId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IWorkspaceRepository(IBaseRepository[Workspace, WorkspaceId]):
    @abstractmethod
    async def find_by_owner_id(self, owner_id: OwnerId) -> list[Workspace]:
        raise NotImplementedError

    @abstractmethod
    async def assign_role_to_user(
        self, workspace_id: WorkspaceId, user_id: OwnerId, role_id: RoleId
    ) -> None:
        raise NotImplementedError