from src.apps.task.domain import TaskEntity
from src.apps.task.dtos import TaskAttrsWithWorkspace, TaskInputDTO


class TaskMapper:
    @staticmethod
    def dto_to_entity(dto: TaskInputDTO) -> TaskEntity:
        return TaskEntity(
            workspace_id=dto.workspace_id,
            name=dto.name,
            feature_id=dto.feature_id,
            owner_id=dto.owner_id,
            assigned_to=dto.assigned_to,
            due_date=dto.due_date,
            description=dto.description,
            priority=dto.priority,
            status=dto.status,
            tags=dto.tags,
        )

    @staticmethod
    def entity_to_attrs_dto(entity: TaskEntity) -> TaskAttrsWithWorkspace:
        return TaskAttrsWithWorkspace(
            workspace_id=entity.workspace_id,
            feature_id=entity.feature_id,
            owner_id=entity.owner_id,
            assigned_to=entity.assigned_to,
            tags=entity.tags,
        )
