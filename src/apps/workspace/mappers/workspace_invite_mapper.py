from src.apps.workspace.domain.entities.workspace_invite import (
    StatusInvite,
    WorkspaceInvite,
)
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import (
    UpdateWorkspaceInviteAppDTO,
    WorkspaceInviteAppDTO,
)
from src.apps.workspace.mappers.base_mapper import BaseMapper


class WorkspaceInviteMapper(BaseMapper[WorkspaceInvite, WorkspaceInviteAppDTO]):
    @staticmethod
    def dto_to_entity(dto: WorkspaceInviteAppDTO) -> WorkspaceInvite:

        return WorkspaceInvite(
            id=InviteId(dto.id),
            code=dto.code,
            _status=StatusInvite(dto.status),
            created_at=dto.created_at,
            _workspace_id=WorkspaceId(dto.workspace_id),
        )

    @staticmethod
    def update_data(
        existing_invite: WorkspaceInvite, dto: UpdateWorkspaceInviteAppDTO
    ) -> WorkspaceInvite:
        status = dto.status

        if status.value == 'Использована':
            existing_invite.use()
        elif status.value == 'Истекла':
            existing_invite.expire()

        return existing_invite
