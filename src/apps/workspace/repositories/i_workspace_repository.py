from abc import abstractmethod

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import MemberId, OwnerId, RoleId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IWorkspaceRepository(IBaseRepository[Workspace, WorkspaceId]):
    @abstractmethod
    async def find_by_member_id(self, member_id: MemberId) -> list[Workspace]:
        raise NotImplementedError

    @abstractmethod
    async def assign_role_to_user(
        self, workspace_id: WorkspaceId, user_id: OwnerId, role_id: RoleId
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_member(self, workspace_id: WorkspaceId, user_id: MemberId) -> None:
        raise NotImplementedError
