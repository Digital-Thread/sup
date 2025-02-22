from abc import ABC, abstractmethod

from src.apps.permission.domain import UserId, PermissionCode, WorkspaceId
from src.apps.permission.dtos import PermissionOutputDTO


class IPermissionRepository(ABC):

    @abstractmethod
    async def get_permissions(self, exclude_hidden: bool) -> list[PermissionOutputDTO]:
        pass

    @abstractmethod
    async def get_user_permissions(self, user_id: UserId, workspace_id: WorkspaceId) -> set[PermissionCode]:
        pass
