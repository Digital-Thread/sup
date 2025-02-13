from src.apps.task.domain import FeatureId
from src.apps.task.dtos import TaskOutputDTO
from src.apps.task.interactors.base_interactor import BaseInteractor
from src.apps.task.query_parameters import TaskListQuery


class GetAllTasksInteractor(BaseInteractor):
    async def execute(
            self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[TaskOutputDTO] | None:
        tasks = await self._repository.get_list(feature_id=feature_id, query=query)
        return (
            [TaskOutputDTO.from_entity(*task) for task in tasks] if tasks else None
        )
