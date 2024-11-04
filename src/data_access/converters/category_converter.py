from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.data_access.models.workspace_models.category import CategoryModel


class CategoryConverter:
    @staticmethod
    def model_to_entity(category_model: CategoryModel) -> Category:
        category = Category(
            _id=CategoryId(category_model.id),
            _name=category_model.name,
            _workspace_id=WorkspaceId(category_model.workspace_id),
        )
        return category

    @staticmethod
    def entity_to_model(category: Category) -> CategoryModel:
        model = CategoryModel(
            id=category.id,
            name=category.name,
            workspace_id=category.workspace_id,
        )
        return model

    @staticmethod
    def entity_to_dict(category: Category) -> dict[str, str | CategoryId | WorkspaceId]:
        return {
            'id': category.id,
            'name': category.name,
            'workspace_id': category.workspace_id,
        }
