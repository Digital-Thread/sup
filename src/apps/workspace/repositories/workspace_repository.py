from abc import abstractmethod

from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
from src.apps.workspace.domain.types_ids import MemberId, OwnerId, WorkspaceId


class IWorkspaceRepository:
    @abstractmethod
    async def save(self, workspace: WorkspaceEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, workspace_id: WorkspaceId) -> WorkspaceEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, workspace: WorkspaceEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, workspace_id: WorkspaceId, owner_id: OwnerId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_workspace_members(self) -> dict[MemberId, str]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_member_id(self, member_id: MemberId) -> list[WorkspaceEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add_member(self, workspace_id: WorkspaceId, user_id: MemberId) -> None:
        raise NotImplementedError
