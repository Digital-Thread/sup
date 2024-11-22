from src.apps.task.domain import AssignedId, FeatureId, OwnerId, TagId, Task, WorkspaceId
from src.data_access.models import TaskModel


class TaskConverter:
    MODEL = TaskModel

    async def map_entity_to_model(self, task_entity: Task) -> TaskModel:
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
            priority=task_entity.priority,
            status=task_entity.status,
        )
        return task_model

    @staticmethod
    def map_model_to_entity(task_model: TaskModel) -> Task:
        task = Task(
            workspace_id=WorkspaceId(task_model.workspace_id),
            name=task_model.name,
            feature_id=FeatureId(task_model.feature_id),
            owner_id=OwnerId(task_model.owner_id),
            assigned_to=(
                AssignedId(task_model.assigned_to_id) if task_model.assigned_to_id else None
            ),
            due_date=task_model.due_date,
            description=task_model.description,
            priority=task_model.priority,
            status=task_model.status,
            tags=[TagId(tag.id) for tag in task_model.tags] if task_model.tags else None,
        )
        task.created_at = task_model.created_at
        task.updated_at = task_model.updated_at
        return task
