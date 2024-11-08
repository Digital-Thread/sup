from uuid import UUID

from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteNotFound,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class GetWorkspaceIdByInviteCodeUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, code: UUID) -> tuple[WorkspaceId, InviteId]:
        try:
            workspace_and_invite_ids = await self._workspaceInvite_repository.find_by_code(code)
        except WorkspaceInviteNotFound:
            raise ValueError(f'Ссылка приглашения не найдена')
        else:
            return workspace_and_invite_ids
