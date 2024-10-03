from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class UpdateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, workspace_invite_id: int, update_data: dict[str, str]) -> None:
        """
        Используем метод с полной загрузкой объекта из БД
        """
        workspace_invite = await self._workspace_invite_repository.find_by_id(workspace_invite_id)
        if update_data.get('status'):
            if workspace_invite.is_expired():
                workspace_invite.expire()
            else:
                workspace_invite.use()

        await self._workspace_invite_repository.update(workspace_invite, update_data)
