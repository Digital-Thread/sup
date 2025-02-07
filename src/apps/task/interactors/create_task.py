from src.apps.task import TaskInputDTO
from src.apps.task.domain import Task
from src.apps.task.exceptions import RepositoryError, TaskCreateError
from src.apps.task.interactors.base_interactor import BaseInteractor


class CreateTaskInteractor(BaseInteractor):
    async def execute(self, dto: TaskInputDTO) -> None:
        try:
            task = Task(
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
        except ValueError as e:
            raise TaskCreateError(context=e) from None

        try:
            await self._repository.save(task=task)
        except RepositoryError as e:
            raise TaskCreateError(context=e) from None
