from src.apps.feature import FeaturesInWorkspaceOutputDTO, FeatureMember
from src.data_access.models.feature import Priority as DB_Priority
from src.data_access.models.feature import Status as DB_Status
from src.apps.feature.domain import (
    FeatureEntity,
    OwnerId,
    ProjectId,
    TagId,
    UserId,
    WorkspaceId,
    FeatureId,
    TaskId,
    Priority,
    Status,
)
from src.data_access.models import FeatureModel


class FeatureMapper:
    MODEL = FeatureModel

    async def map_entity_to_model(self, feature_entity: FeatureEntity) -> FeatureModel:
        feature_model = self.MODEL(
            workspace_id=feature_entity.workspace_id,
            name=feature_entity.name,
            project_id=feature_entity.project_id,
            owner_id=feature_entity.owner_id,
            created_at=feature_entity.created_at,
            updated_at=feature_entity.updated_at,
            assigned_to_id=feature_entity.assigned_to,
            description=feature_entity.description,
            priority=DB_Priority[feature_entity.priority.name],
            status=DB_Status[feature_entity.status.name],
        )
        return feature_model

    @staticmethod
    def map_model_to_entity(feature_model: FeatureModel, with_tasks: bool) -> FeatureEntity:
        feature = FeatureEntity(
            workspace_id=WorkspaceId(feature_model.workspace_id),
            name=feature_model.name,
            project_id=ProjectId(feature_model.project_id),
            owner_id=OwnerId(feature_model.owner_id),
            assigned_to=(
                UserId(feature_model.assigned_to_id) if feature_model.assigned_to_id else None
            ),
            description=feature_model.description,
            priority=Priority[DB_Priority(feature_model.priority).name],
            status=Status[DB_Status(feature_model.status).name],
            tags=[TagId(tag.id) for tag in feature_model.tags] if feature_model.tags else None,
            members=(
                [UserId(user.id) for user in feature_model.members]
                if feature_model.members
                else None
            ),
        )
        if with_tasks:
            feature.tasks = ([TaskId(task.id) for task in feature_model.tasks] if feature_model.tasks else None)

        feature.id = FeatureId(feature_model.id)
        feature.created_at = feature_model.created_at
        feature.updated_at = feature_model.updated_at
        return feature

    @staticmethod
    def map_model_to_workspace_dto(feature_model: FeatureModel) -> FeaturesInWorkspaceOutputDTO:
        return FeaturesInWorkspaceOutputDTO(
            id=FeatureId(feature_model.id),
            name=feature_model.name,
            project_name=feature_model.project.name,
            created_at=feature_model.created_at,
            priority=Priority[DB_Priority(feature_model.priority).name],
            status=Status[DB_Status(feature_model.status).name],
            members=[
                {'id': UserId(user.id),
                 'fullname': user.first_name + ' ' + user.last_name,
                 'avatar': user.avatar
                 }
                for user in feature_model.members]
            if feature_model.members
            else None
        )
