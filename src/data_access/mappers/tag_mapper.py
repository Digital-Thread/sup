from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.data_access.models.workspace_models.tag import TagModel


class TagMapper:
    @staticmethod
    def model_to_entity(tag_model: TagModel) -> TagEntity:
        return TagEntity(
            _id=TagId(tag_model.id),
            _name=tag_model.name,
            _color=tag_model.color,
            _workspace_id=WorkspaceId(tag_model.workspace_id),
        )

    @staticmethod
    def entity_to_model(entity: TagEntity) -> TagModel:
        model = TagModel(
            id=entity.id,
            name=entity.name,
            color=entity.color,
            workspace_id=entity.workspace_id,
        )
        return model

    @staticmethod
    def entity_to_dict(tag: TagEntity) -> dict[str, str | TagId | WorkspaceId]:
        return {
            'id': tag.id,
            'name': tag.name,
            'color': tag.color,
            'workspace_id': tag.workspace_id,
        }
