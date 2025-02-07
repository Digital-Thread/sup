from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import (
    GetWorkspaceInvitesDTO,
    WorkspaceInviteOutDTO,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class GetWorkspaceInvitesByWorkspaceInteractor:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, request_data: GetWorkspaceInvitesDTO) -> list[WorkspaceInviteOutDTO]:
        workspace_invites = await self._workspace_invite_repository.get_by_workspace_id(
            workspace_id=WorkspaceId(request_data.workspace_id),
            page=request_data.page,
            page_size=request_data.page_size,
        )
        return [
            WorkspaceInviteMapper.entity_to_dto(workspace_invite, WorkspaceInviteOutDTO)
            for workspace_invite in workspace_invites
        ]
