from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import WorkspaceInviteAppDTO
from src.apps.workspace.exceptions.workspace_invite_exceptions import (
    WorkspaceWorkspaceInviteNotFound,
)
from src.apps.workspace.mappers.workspace_invite_mapper import WorkspaceInviteMapper
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)


class GetWorkspaceInviteByWorkspaceUseCase:
    def __init__(self, workspace_invite_repository: IWorkspaceInviteRepository):
        self._workspace_invite_repository = workspace_invite_repository

    async def execute(self, workspace_id: WorkspaceId) -> list[WorkspaceInviteAppDTO]:
        try:
            workspace_invites = await self._workspace_invite_repository.find_by_workspace_id(
                workspace_id
            )
        except WorkspaceWorkspaceInviteNotFound:
            raise ValueError(
                f'Рабочее пространство с id={workspace_id} для ссылки приглашения не найдено'
            )
        else:
            return [
                WorkspaceInviteMapper.entity_to_dto(workspace_invite, WorkspaceInviteAppDTO)
                for workspace_invite in workspace_invites
            ]
