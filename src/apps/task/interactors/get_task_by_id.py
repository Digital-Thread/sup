from src.apps.task import TaskOutputDTO
from src.apps.task.domain import TaskId
from src.apps.task.exceptions import TaskDoesNotExistError
from src.apps.task.interactors.base_interactor import BaseInteractor


class GetTaskByIdInteractor(BaseInteractor):
    async def execute(self, task_id: TaskId) -> TaskOutputDTO:
        task = await self._repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskDoesNotExistError(task_id)

        task_dto = TaskOutputDTO.from_entity(entity=task)
        return task_dto
