from src.apps.task.domain import FeatureId
from src.apps.task.dtos import TaskInFeatureOutputDTO
from src.apps.task.interactors.base_interactor import BaseInteractor
from src.apps.task.query_parameters import TaskListQuery


class GetTasksByFeatureIdInteractor(BaseInteractor):
    async def execute(
        self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[TaskInFeatureOutputDTO]:
        tasks = await self._repository.get_by_feature_id(feature_id=feature_id, query=query)
        return tasks
