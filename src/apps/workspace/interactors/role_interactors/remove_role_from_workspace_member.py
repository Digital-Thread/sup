from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId, MemberId
from src.apps.workspace.dtos.role_dtos import RemoveRoleFromWorkspaceMemberDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException, RoleNotFoundForWorkspaceMember
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceNotFound, WorkspaceMemberNotFound
from src.apps.workspace.repositories.user_workspace_role_repository import IUserWorkspaceRoleRepository


class RemoveRoleFromWorkspaceMemberInteractor:
    def __init__(self, user_workspace_role_repository: IUserWorkspaceRoleRepository):
        self._user_workspace_role_repository = user_workspace_role_repository

    async def execute(self, request_data: RemoveRoleFromWorkspaceMemberDTO) -> None:
        try:
            await self._user_workspace_role_repository.remove_role_from_workspace_member(WorkspaceId(request_data.workspace_id), MemberId(request_data.member_id))
        except (RoleNotFoundForWorkspaceMember, WorkspaceNotFound, WorkspaceMemberNotFound) as error:
            raise RoleException(f'{str(error)}')
