from src.apps.task import (
    TaskOutputDTO,
    TaskInFeatureOutputDTO,
    TaskTag,
    FeatureInfo,
    TaskMember,
)
from src.apps.task.domain import (
    AssignedId,
    FeatureId,
    OwnerId,
    TagId,
    TaskEntity,
    WorkspaceId,
    Priority,
    Status,
    UserId,
    TaskId,
)

from src.data_access.models import TaskModel
from src.data_access.models.task import Priority as DB_Priority
from src.data_access.models.task import Status as DB_Status


class TaskMapper:
    MODEL = TaskModel

    async def map_entity_to_model(self, task_entity: TaskEntity) -> TaskModel:
        task_model = self.MODEL(
            workspace_id=task_entity.workspace_id,
            name=task_entity.name,
            feature_id=task_entity.feature_id,
            owner_id=task_entity.owner_id,
            assigned_to_id=task_entity.assigned_to,
            due_date=task_entity.due_date,
            created_at=task_entity.created_at,
            updated_at=task_entity.updated_at,
            description=task_entity.description,
            priority=DB_Priority[task_entity.priority.name],
            status=DB_Status[task_entity.status.name],
        )
        return task_model

    @staticmethod
    def map_model_to_entity(task_model: TaskModel) -> TaskEntity:
        task = TaskEntity(
            workspace_id=WorkspaceId(task_model.workspace_id),
            name=task_model.name,
            feature_id=FeatureId(task_model.feature_id),
            owner_id=OwnerId(task_model.owner_id),
            assigned_to=(
                AssignedId(task_model.assigned_to_id) if task_model.assigned_to_id else None
            ),
            due_date=task_model.due_date,
            description=task_model.description,
            priority=Priority[DB_Priority(task_model.priority).name],
            status=Status[DB_Status(task_model.status).name],
            tags=[TagId(tag.id) for tag in task_model.tags] if task_model.tags else None,
        )
        task.id = task_model.id
        task.created_at = task_model.created_at
        task.updated_at = task_model.updated_at
        return task

    @staticmethod
    def map_model_to_dto(task_model: TaskModel) -> TaskOutputDTO:
        dto = TaskOutputDTO(
            id=TaskId(task_model.id),
            name=task_model.name,
            owner=TaskMember(
                id=UserId(task_model.owner_id),
                fullname=task_model.owner.first_name + ' ' + task_model.owner.last_name,
                avatar=task_model.owner.avatar,
            ),
            feature=FeatureInfo(
                id=FeatureId(task_model.feature_id),
                name=task_model.feature.name
            ),
            feature_lead=TaskMember(
                id=UserId(task_model.feature.owner_id),
                fullname=task_model.feature.owner.first_name + ' ' + task_model.feature.owner.last_name,
                avatar=task_model.feature.owner.avatar,
            ),
            assigned_to=TaskMember(
                id=UserId(task_model.assigned_to_id),
                fullname=task_model.assigned_to.first_name + ' ' + task_model.assigned_to.last_name,
                avatar=task_model.assigned_to.avatar,
            ),
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
            due_date=task_model.due_date,
            description=task_model.description,
            priority=Priority[DB_Priority(task_model.priority).name],
            status=Status[DB_Status(task_model.status).name],
            tags=(
                [
                    TaskTag(
                        id=TagId(tag.id),
                        name=tag.name,
                        color=tag.color)
                    for tag in task_model.tags
                ]
                if task_model.tags
                else None
            ),
        )

        return dto

    @staticmethod
    def map_model_to_for_feature_dto(task_model: TaskModel) -> TaskInFeatureOutputDTO:
        dto = TaskInFeatureOutputDTO(
            id=TaskId(task_model.id),
            name=task_model.name,
            assigned_to=TaskMember(
                id=UserId(task_model.assigned_to_id),
                fullname=task_model.assigned_to.first_name + ' ' + task_model.assigned_to.last_name,
                avatar=task_model.assigned_to.avatar,
            ),
            created_at=task_model.created_at,
            due_date=task_model.due_date,
            priority=Priority[DB_Priority(task_model.priority).name],
            status=Status[DB_Status(task_model.status).name],
        )

        return dto
