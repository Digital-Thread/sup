from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryOutDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class CategoryMapper(BaseMapper[CategoryEntity, CategoryOutDTO]):
    @staticmethod
    def dto_to_entity(dto: CategoryOutDTO) -> CategoryEntity:

        return CategoryEntity(
            _id=CategoryId(dto.id),
            _workspace_id=WorkspaceId(dto.workspace_id),
            _name=dto.name,
        )
