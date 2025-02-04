from src.apps.feature.domain import FeatureEntity, FeatureId
from src.apps.feature.dtos import FeatureInputDTO, FeatureOutputDTO


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
