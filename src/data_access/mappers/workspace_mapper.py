from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
from src.apps.workspace.domain.types_ids import (
    OwnerId,
    WorkspaceId,
)
from src.data_access.models.workspace_models.workspace import WorkspaceModel


class WorkspaceMapper:

    @staticmethod
    def model_to_entity(workspace_model: WorkspaceModel) -> WorkspaceEntity:
        return WorkspaceEntity(
            owner_id=OwnerId(workspace_model.owner_id),
            _name=workspace_model.name,
            _id=WorkspaceId(workspace_model.id),
            _description=workspace_model.description,
            logo=workspace_model.logo,
            created_at=workspace_model.created_at,
        )

    @staticmethod
    def entity_to_model(entity: WorkspaceEntity) -> WorkspaceModel:
        model = WorkspaceModel(
            id=entity.id,
            owner_id=entity.owner_id,
            name=entity.name,
            description=entity.description,
            logo=entity.logo,
            created_at=entity.created_at,
        )
        return model

    @staticmethod
    def entity_to_dict(workspace: WorkspaceEntity) -> dict[str, str]:
        return {
            'name': workspace.name,
            'description': workspace.description,
            'logo': workspace.logo,
        }
