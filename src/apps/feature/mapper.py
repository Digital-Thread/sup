from src.apps.feature.domain import FeatureEntity
from src.apps.feature.dtos import FeatureInputDTO, FeatureAttrsWithWorkspace


class FeatureMapper:
    @staticmethod
    def dto_to_entity(dto: FeatureInputDTO) -> FeatureEntity:
        return FeatureEntity(
            workspace_id=dto.workspace_id,
            name=dto.name,
            project_id=dto.project_id,
            owner_id=dto.owner_id,
            assigned_to=dto.assigned_to,
            description=dto.description,
            priority=dto.priority,
            status=dto.status,
            tags=dto.tags,
            members=dto.members,
        )

    @staticmethod
    def entity_to_attrs_dto(entity: FeatureEntity) -> FeatureAttrsWithWorkspace:
        return FeatureAttrsWithWorkspace(
            workspace_id=entity.workspace_id,
            project_id=entity.project_id,
            owner_id=entity.owner_id,
            assigned_to=entity.assigned_to,
            tags=entity.tags,
            members=entity.members
        )
