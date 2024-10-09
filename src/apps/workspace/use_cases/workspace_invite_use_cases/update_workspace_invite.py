from src.apps.workspace.dtos.workspace_invite_dtos import UpdateWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class UpdateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(
        self, workspace_invite_id: int, update_data: UpdateWorkspaceInviteAppDTO
    ) -> None:
        """
        Используем метод с полной загрузкой объекта из БД
        """
        try:
            workspace_invite = await self._workspace_invite_repository.find_by_id(
                workspace_invite_id
            )
        except WorkspaceInviteNotFound:
            raise WorkspaceInviteNotFound

        if update_data.get('status'):
            if workspace_invite.is_expired():
                workspace_invite.expire()
            else:
                workspace_invite.use()

        await self._workspace_invite_repository.update(workspace_invite)
