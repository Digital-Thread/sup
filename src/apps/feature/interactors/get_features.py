from src.apps.feature.query_parameters import FeatureListQuery
from src.apps.feature.mapper import FeatureMapper
from src.apps.feature.domain import WorkspaceId
from src.apps.feature.dtos import FeatureOutputDTO
from src.apps.feature.interactors.base_interactor import BaseInteractor


class GetAllFeaturesInteractor(BaseInteractor):
    async def execute(
            self, workspace_id: WorkspaceId, query: FeatureListQuery
    ) -> list[FeatureOutputDTO] | None:
        features = await self._repository.get_list(workspace_id=workspace_id, query=query)
        return (
            [FeatureMapper.entity_to_dto(*feature) for feature in features] if features else None
        )
