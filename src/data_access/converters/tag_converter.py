from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.data_access.models.workspace_models.tag import TagModel


class TagConverter:
    @staticmethod
    def model_to_entity(tag_model: TagModel) -> Tag:
        return Tag(
            _id=tag_model.id,
            _name=tag_model.name,
            _color=tag_model.color,
            _workspace_id=WorkspaceId(tag_model.workspace_id),
        )

    @staticmethod
    def entity_to_model(entity: Tag) -> TagModel:
        model = TagModel(**entity.__dict__)
        return model

    @staticmethod
    def entity_to_dict(tag: Tag) -> dict:
        return {
            'id': tag.id,
            'name': tag.name,
            'color': tag.color,
            'workspace_id': tag.workspace_id,
        }
