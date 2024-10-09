from src.apps.workspace.domain.entities.workspace_invite import (
    StatusInvite,
    WorkspaceInvite,
)
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import CreateWorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteAlreadyExists,
)
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class CreateWorkspaceInviteUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspaceInvite_repository = workspace_invite_repository

    async def execute(self, workspace_invite_data: CreateWorkspaceInviteAppDTO) -> None:
        workspace_invite = WorkspaceInvite(
            _workspace_id=WorkspaceId(workspace_invite_data['workspace_id']),
            code=workspace_invite_data['code'],
            _status=StatusInvite(workspace_invite_data['status']),
            created_at=workspace_invite_data['created_at'],
        )

        try:
            await self._workspaceInvite_repository.save(workspace_invite)
        except WorkspaceInviteAlreadyExists:
            raise ValueError(f'Ссылка приглашения {workspace_invite.code} уже существует')
