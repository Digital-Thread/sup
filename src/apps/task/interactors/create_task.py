from src.apps.task import TaskInputDTO
from src.apps.task.exceptions import TaskCreateError, TaskRepositoryError
from src.apps.task.interactors.base_interactor import BaseInteractor
from src.apps.task.mapper import TaskMapper


class CreateTaskInteractor(BaseInteractor):
    async def execute(self, dto: TaskInputDTO) -> None:
        try:
            task = TaskMapper.dto_to_entity(dto=dto)
        except ValueError as e:
            raise TaskCreateError(context=e) from None

        try:
            attrs = TaskMapper.entity_to_attrs_dto(task)
            await self._repository.validate_workspace_consistency(attrs=attrs)
        except TaskRepositoryError as e:
            raise TaskCreateError(context=e) from None

        try:
            await self._repository.save(task=task)
        except TaskRepositoryError as e:
            raise TaskCreateError(context=e) from None
