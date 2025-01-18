from src.apps.feature.domain import FeatureEntity, FeatureId
from src.apps.feature.dtos import FeatureInputDTO, FeatureOutputDTO


class FeatureMapper:

    @staticmethod
    def entity_to_dto(
        entity: FeatureEntity,
    ) -> FeatureOutputDTO:
        return FeatureOutputDTO(
            id=entity.id,
            workspace_id=entity.workspace_id,
            name=entity.name,
            project_id=entity.project_id,
            owner_id=entity.owner_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            assigned_to=entity.assigned_to,
            description=entity.description,
            priority=entity.priority,
            status=entity.status,
            tags=entity.tags,
            members=entity.members,
            tasks=entity.tasks,
        )

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
