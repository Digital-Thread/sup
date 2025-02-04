from src.apps.feature.mapper import FeatureMapper
from src.apps.feature import FeatureOutputDTO
from src.apps.feature.domain import FeatureId
from src.apps.feature.exceptions import FeatureDoesNotExistError
from src.apps.feature.interactors.base_interactor import BaseInteractor


class GetFeatureByIdInteractor(BaseInteractor):
    async def execute(self, feature_id: FeatureId) -> FeatureOutputDTO:
        feature = await self._repository.get_by_id(feature_id=feature_id)
        if not feature:
            raise FeatureDoesNotExistError(feature_id)

        return feature
