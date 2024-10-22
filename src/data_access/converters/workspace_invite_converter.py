from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.data_access.models.workspace_models.workspace_invite import (
    WorkspaceInviteModel,
)


class WorkspaceInviteConverter[T]:
    @staticmethod
    def model_to_entity(workspace_invite_model: T) -> WorkspaceInvite:
        clean_data = {
            column.name: getattr(workspace_invite_model, column.name)
            for column in workspace_invite_model.__table__.columns
        }
        invite = WorkspaceInvite(
            id=clean_data['id'],
            code=clean_data['code'],
            _status=clean_data['status'],
            _workspace_id=clean_data['workspace_id'],
            created_at=clean_data['created_at'],
        )
        return invite

    @staticmethod
    def entity_to_model(entity: WorkspaceInvite) -> WorkspaceInviteModel:
        model = WorkspaceInviteModel(**entity.__dict__)
        return model
