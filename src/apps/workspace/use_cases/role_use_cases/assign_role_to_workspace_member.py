from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId, MemberId, RoleId
from src.apps.workspace.exceptions.role_exceptions import RoleNotFound, RoleException
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceNotFound, WorkspaceMemberNotFound, \
    WorkspaceException
from src.apps.workspace.repositories.i_user_workspace_role_repository import IUserWorkspaceRoleRepository


class AssignRoleToWorkspaceMemberUseCase:
    def __init__(self, user_workspace_role_repository: IUserWorkspaceRoleRepository):
        self._user_workspace_role_repository = user_workspace_role_repository

    async def execute(self, workspace_id: UUID, member_id: UUID, role_id: int) -> None:
        try:
            await self._user_workspace_role_repository.assign_role_to_workspace_member(WorkspaceId(workspace_id), MemberId(member_id), RoleId(role_id))
        except (WorkspaceNotFound, RoleNotFound, WorkspaceMemberNotFound) as error:
            raise RoleException(f'{str(error)}')
