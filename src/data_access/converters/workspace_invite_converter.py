from src.apps.workspace.domain.entities.workspace_invite import (
    StatusInvite,
    WorkspaceInvite,
)
from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId
from src.data_access.models.workspace_models.workspace_invite import (
    WorkspaceInviteModel,
)


class WorkspaceInviteConverter:
    @staticmethod
    def model_to_entity(workspace_invite_model: WorkspaceInviteModel) -> WorkspaceInvite:
        return WorkspaceInvite(
            id=InviteId(workspace_invite_model.id),
            code=workspace_invite_model.code,
            _status=StatusInvite(workspace_invite_model.status),
            _workspace_id=WorkspaceId(workspace_invite_model.workspace_id),
            created_at=workspace_invite_model.created_at,
        )

    @staticmethod
    def entity_to_model(workspace_invite: WorkspaceInvite) -> WorkspaceInviteModel:
        model = WorkspaceInviteModel(
            id=workspace_invite.id,
            code=workspace_invite.code,
            status=workspace_invite.status.value,
            created_at=workspace_invite.created_at,
            expired_at=workspace_invite.expired_at,
            workspace_id=workspace_invite.workspace_id,
        )
        return model

    @staticmethod
    def entity_to_dict(workspace_invite: WorkspaceInvite) -> dict[str, StatusInvite]:
        return {
            'status': workspace_invite.status.value,
        }
