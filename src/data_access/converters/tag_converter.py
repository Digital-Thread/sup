from src.apps.workspace.domain.entities.tag import Tag
from src.data_access.models.workspace_models.tag import TagModel


class TagConverter[T]:
    @staticmethod
    def model_to_entity(tag_model: T) -> Tag:
        clean_data = {
            column.name: getattr(tag_model, column.name) for column in tag_model.__table__.columns
        }
        role = Tag(
            _id=clean_data['id'],
            _name=clean_data['name'],
            _color=clean_data['color'],
            _workspace_id=clean_data['workspace_id'],
        )
        return role

    @staticmethod
    def entity_to_model(entity: Tag) -> TagModel:
        model = TagModel(**entity.__dict__)
        return model
