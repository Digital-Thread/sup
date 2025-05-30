from src.apps.workspace.domain.types_ids import MemberId, RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import AssignRoleToWorkspaceMemberDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException, RoleNotFound
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceMemberNotFound,
    WorkspaceNotFound,
)
from src.apps.workspace.repositories.user_workspace_role_repository import (
    IUserWorkspaceRoleRepository,
)


class AssignRoleToWorkspaceMemberInteractor:
    def __init__(self, user_workspace_role_repository: IUserWorkspaceRoleRepository):
        self._user_workspace_role_repository = user_workspace_role_repository

    async def execute(self, request_data: AssignRoleToWorkspaceMemberDTO) -> None:
        try:
            await self._user_workspace_role_repository.assign_role_to_workspace_member(
                member_id=MemberId(request_data.member_id),
                role_id=RoleId(request_data.id),
                workspace_id=WorkspaceId(request_data.workspace_id),
            )
        except (WorkspaceNotFound, RoleNotFound, WorkspaceMemberNotFound) as error:
            raise RoleException(f'{str(error)}')
