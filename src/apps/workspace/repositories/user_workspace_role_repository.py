from abc import ABC, abstractmethod

from src.apps.workspace.domain.types_ids import MemberId, RoleId, WorkspaceId


class IUserWorkspaceRoleRepository(ABC):

    @abstractmethod
    async def assign_role_to_workspace_member(
        self, member_id: MemberId, role_id: RoleId, workspace_id: WorkspaceId
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_role_from_workspace_member(
        self, member_id: MemberId, workspace_id: WorkspaceId
    ) -> None:
        raise NotImplementedError
