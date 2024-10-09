from typing import Any

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryAppDTO, UpdateCategoryAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class CategoryMapper(BaseMapper[Category, CategoryAppDTO]):
    @staticmethod
    def dto_to_entity(
        dto: CategoryAppDTO | UpdateCategoryAppDTO, immutable_data: dict[str, Any]
    ) -> Category:

        if isinstance(dto, CategoryAppDTO):
            category = Category(
                _id=CategoryId(dto.id),
                _workspace_id=WorkspaceId(dto.workspace_id),
                _name=dto.name,
            )

        else:
            category = Category(
                _id=immutable_data['category_id'],
                _workspace_id=immutable_data['workspace_id'],
                _name=dto['name'],
            )

        return category
