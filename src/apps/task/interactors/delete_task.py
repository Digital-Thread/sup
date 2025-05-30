from src.apps.task.domain import TaskId
from src.apps.task.exceptions import TaskDeleteError, TaskRepositoryError
from src.apps.task.interactors.base_interactor import BaseInteractor


class DeleteTaskInteractor(BaseInteractor):
    async def execute(self, task_id: TaskId) -> None:
        try:
            await self._repository.delete(task_id=task_id)
        except TaskRepositoryError as e:
            raise TaskDeleteError(context=e) from None
        else:
            await self._repository.delete_comments(task_id=task_id)
