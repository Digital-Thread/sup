from src.apps.task.mapper import TaskMapper
from src.apps.task import TaskInputDTO
from src.apps.task.exceptions import RepositoryError, TaskCreateError
from src.apps.task.interactors.base_interactor import BaseInteractor


class CreateTaskInteractor(BaseInteractor):
    async def execute(self, dto: TaskInputDTO) -> None:
        try:
            task = TaskMapper.dto_to_entity(dto=dto)
        except ValueError as e:
            raise TaskCreateError(context=e) from None

        try:
            await self._repository.save(task=task)
        except RepositoryError as e:
            raise TaskCreateError(context=e) from None
