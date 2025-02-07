from src.apps.task.dtos import TaskUpdateDTO
from src.apps.task.exceptions import RepositoryError, TaskDoesNotExistError, TaskUpdateError
from src.apps.task.interactors.base_interactor import BaseInteractor


class UpdateTaskInteractor(BaseInteractor):
    async def execute(self, dto: TaskUpdateDTO) -> None:
        task = await self._repository.get_by_id(task_id=dto.id)
        if not task:
            raise TaskDoesNotExistError(dto.id)

        try:
            task.update_fields(dto.updated_fields)
        except ValueError as e:
            raise TaskUpdateError(context=e) from None

        try:
            await self._repository.update(task_id=dto.id, task=task)
        except RepositoryError as e:
            raise TaskUpdateError(context=e) from None
