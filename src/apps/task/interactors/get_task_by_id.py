from src.apps.task.dtos import TaskOutputDTO
from src.apps.task.domain import TaskId
from src.apps.task.exceptions import TaskDoesNotExistError
from src.apps.task.interactors.base_interactor import BaseInteractor


class GetTaskByIdInteractor(BaseInteractor):
    async def execute(self, task_id: TaskId) -> TaskOutputDTO:
        task_dto = await self._repository.get_by_id(task_id=task_id)
        if not task_dto:
            raise TaskDoesNotExistError(task_id)

        return task_dto
