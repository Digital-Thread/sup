from src.apps.feature import FeatureOutputDTO
from src.apps.feature.domain import FeatureId
from src.apps.feature.exceptions import FeatureDoesNotExistError
from src.apps.feature.interactors.base_interactor import BaseInteractor


class GetFeatureInteractor(BaseInteractor):
    async def execute(self, feature_id: FeatureId) -> FeatureOutputDTO:
        feature = await self._repository.get_by_id(feature_id=feature_id)
        if not feature:
            raise FeatureDoesNotExistError(feature_id)

        feature_dto = FeatureOutputDTO.from_entity(feature_id=feature_id, entity=feature)
        return feature_dto
