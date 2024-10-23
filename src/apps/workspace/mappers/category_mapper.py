from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryAppDTO, UpdateCategoryAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class CategoryMapper(BaseMapper[Category, CategoryAppDTO]):
    @staticmethod
    def dto_to_entity(dto: CategoryAppDTO) -> Category:

        return Category(
            _id=CategoryId(dto.id),
            _workspace_id=WorkspaceId(dto.workspace_id),
            _name=dto.name,
        )

    @staticmethod
    def update_data(existing_category: Category, dto: UpdateCategoryAppDTO) -> Category:
        existing_category.name = dto.get('name')
        return existing_category
