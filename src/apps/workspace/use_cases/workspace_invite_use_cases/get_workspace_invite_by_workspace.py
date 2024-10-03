from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class GetWorkspaceInviteByWorkspaceUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, workspace_id: UUID) -> list[WorkspaceInvite]:
        try:
            workspace_invites = await self._workspace_invite_repository.find_by_workspace_id(
                workspace_id
            )
        except WorkspaceWorkspaceInviteNotFound:
            raise ValueError(
                f'Рабочее пространство с id={workspace_id} для ссылки приглашения не найдено'
            )

        return workspace_invites
