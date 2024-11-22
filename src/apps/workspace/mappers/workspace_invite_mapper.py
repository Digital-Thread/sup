from src.apps.workspace.domain.entities.workspace_invite import (
    StatusInvite,
    WorkspaceInviteEntity,
)
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.apps.workspace.dtos.workspace_invite_dtos import (
    UpdateWorkspaceInviteAppDTO,
    WorkspaceInviteAppDTO,
)
from src.apps.workspace.mappers.base_mapper import BaseMapper


class WorkspaceInviteMapper(BaseMapper[WorkspaceInviteEntity, WorkspaceInviteAppDTO]):
    @staticmethod
    def dto_to_entity(dto: WorkspaceInviteAppDTO) -> WorkspaceInviteEntity:

        return WorkspaceInviteEntity(
            _id=InviteId(dto.id),
            code=dto.code,
            _status=StatusInvite(dto.status),
            created_at=dto.created_at,
            _workspace_id=WorkspaceId(dto.workspace_id),
        )

    @staticmethod
    def update_data(
        existing_invite: WorkspaceInviteEntity, dto: UpdateWorkspaceInviteAppDTO
    ) -> WorkspaceInviteEntity:
        status = dto.status

        if status.value == 'Использована':
            existing_invite.use()
        elif status.value == 'Истекла':
            existing_invite.expire()

        return existing_invite
