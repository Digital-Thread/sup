from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import WorkspaceInviteAppDTO, GetWorkspaceInvitesAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceInviteException,
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class GetWorkspaceInviteByWorkspaceInteractor:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, request_data: GetWorkspaceInvitesAppDTO) -> list[WorkspaceInviteAppDTO]:
        try:
            workspace_invites = await self._workspace_invite_repository.find_by_workspace_id(
                WorkspaceId(request_data.workspace_id)
            )
        except WorkspaceWorkspaceInviteNotFound as error:
            raise WorkspaceInviteException(f'{str(error)}')
        else:
            return [
                WorkspaceInviteMapper.entity_to_dto(workspace_invite, WorkspaceInviteAppDTO)
                for workspace_invite in workspace_invites
            ]
