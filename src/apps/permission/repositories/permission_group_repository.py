from abc import ABC, abstractmethod

from src.apps.permission.dtos import PermissionGroupOutputDTO
from src.apps.permission.domain import PermissionGroupEntity, WorkspaceId, PermissionGroupId, UserId


class IPermissionGroupRepository(ABC):

    @abstractmethod
    async def save(self, perm_group: PermissionGroupEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_perm_group_entity(self, perm_group_id: PermissionGroupId) -> PermissionGroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_perm_group_by_id(self, perm_group_id: PermissionGroupId) -> PermissionGroupOutputDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_perm_groups_by_workspace_id(self, workspace_id: WorkspaceId) -> list[PermissionGroupOutputDTO] | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, perm_group: PermissionGroupEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, perm_group_id: PermissionGroupId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def assign_permission_group(
            self,
            group_name: str,
            user_id: UserId,
            workspace_id: WorkspaceId | None = None,
    ) -> None:
        pass
