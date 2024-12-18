from abc import ABC, abstractmethod

from src.apps.workspace.domain.types_ids import RoleId, MemberId, WorkspaceId


class IUserWorkspaceRoleRepository(ABC):

    @abstractmethod
    async def assign_role_to_workspace_member(self, member_id: MemberId, role_id: RoleId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_role_from_workspace_member(self, member_id: MemberId) -> None:
        raise NotImplementedError
