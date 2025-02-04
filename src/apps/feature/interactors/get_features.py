from src.apps.feature.query_parameters import FeatureListQuery
from src.apps.feature.domain import WorkspaceId
from src.apps.feature.dtos import FeatureInWorkspaceOutputDTO
from src.apps.feature.interactors.base_interactor import BaseInteractor


class GetFeaturesByWorkspaceInteractor(BaseInteractor):
    async def execute(
            self,
            workspace_id: WorkspaceId,
            query: FeatureListQuery,
    ) -> list[FeatureInWorkspaceOutputDTO] | None:
        features = await self._repository.get_by_workspace_id(workspace_id=workspace_id, query=query)
        return features
