from src.apps.feature.domain import Feature, OwnerId, ProjectId, UserId, WorkspaceId
from src.data_access.models import FeatureModel


class FeatureMapper:
    MODEL = FeatureModel

    async def map_entity_to_model(self, feature_entity: Feature) -> FeatureModel:
        feature_model = self.MODEL(
            workspace_id=feature_entity.workspace_id,
            name=feature_entity.name,
            project_id=feature_entity.project_id,
            owner_id=feature_entity.owner_id,
            created_at=feature_entity.created_at,
            updated_at=feature_entity.updated_at,
            assigned_to=feature_entity.assigned_to,
            description=feature_entity.description,
            priority=feature_entity.priority,
            status=feature_entity.status,
        )
        return feature_model

    @staticmethod
    def map_model_to_entity(feature_model: FeatureModel) -> Feature:
        feature = Feature(
            workspace_id=WorkspaceId(feature_model.workspace_id),
            name=feature_model.name,
            project_id=ProjectId(feature_model.project_id),
            owner_id=OwnerId(feature_model.owner_id),
            assigned_to=(
                UserId(feature_model.assigned_to_id) if feature_model.assigned_to_id else None
            ),
            description=feature_model.description,
            priority=feature_model.priority,
            status=feature_model.status,
            tags=[tag.id for tag in feature_model.tags] if feature_model.tags else None,
            members=[user.id for user in feature_model.members] if feature_model.members else None,
        )
        feature.created_at = feature_model.created_at
        feature.updated_at = feature_model.updated_at
        return feature
