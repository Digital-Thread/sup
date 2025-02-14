from src.apps.task.dtos import TaskUpdateDTO
from src.apps.task.exceptions import (
    TaskDoesNotExistError,
    TaskRepositoryError,
    TaskUpdateError,
)
from src.apps.task.interactors.base_interactor import BaseInteractor
from src.apps.task.mapper import TaskMapper


class UpdateTaskInteractor(BaseInteractor):
    async def execute(self, dto: TaskUpdateDTO) -> None:
        task = await self._repository.get_entity(task_id=dto.id)
        if not task:
            raise TaskDoesNotExistError(dto.id)

        try:
            task.update_fields(dto.updated_fields)
        except ValueError as e:
            raise TaskUpdateError(context=e) from None

        try:
            attrs = TaskMapper.entity_to_attrs_dto(task)
            await self._repository.validate_workspace_consistency(attrs=attrs)
        except TaskRepositoryError as e:
            raise TaskUpdateError(context=e) from None

        try:
            await self._repository.update(task_id=dto.id, task=task)
        except TaskRepositoryError as e:
            raise TaskUpdateError(context=e) from None
