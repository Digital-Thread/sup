from src.apps.workspace.domain.entities.category import Category
from src.data_access.models.workspace_models.category import CategoryModel


class CategoryConverter[T]:
    @staticmethod
    def model_to_entity(category_model: T) -> Category:
        clean_data = {
            column.name: getattr(category_model, column.name)
            for column in category_model.__table__.columns
        }
        category = Category(
            _id=clean_data['id'],
            _name=clean_data['name'],
            _workspace_id=clean_data['workspace_id'],
        )
        return category

    @staticmethod
    def entity_to_model(entity: Category) -> CategoryModel:
        model = CategoryModel(**entity.__dict__)
        return model
