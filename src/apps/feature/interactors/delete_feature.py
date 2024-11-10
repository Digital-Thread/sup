from src.apps.feature.domain import FeatureId
from src.apps.feature.exceptions import FeatureDeleteError, RepositoryError
from src.apps.feature.interactors.base_interactor import BaseInteractor


class DeleteFeatureInteractor(BaseInteractor):
    async def execute(self, feature_id: FeatureId) -> None:
        try:
            await self._repository.delete(feature_id=feature_id)
        except RepositoryError as e:
            raise FeatureDeleteError(context=e) from None
