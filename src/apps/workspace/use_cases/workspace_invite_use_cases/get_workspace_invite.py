from src.apps.workspace.dtos.workspace_invite_dtos import WorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class GetWorkspaceInviteByIdUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_invite_id: int) -> WorkspaceInviteAppDTO:
        try:
            workspace_invite = await self._workspaceInvite_repository.find_by_id(
                workspace_invite_id
            )
        except WorkspaceInviteNotFound:
            raise ValueError(f'Тег с id={workspace_invite_id} не найдена')
        else:
            return WorkspaceInviteAppDTO.from_entity(workspace_invite)
