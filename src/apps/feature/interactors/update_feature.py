from src.apps.feature.dtos import FeatureUpdateDTO
from src.apps.feature.exceptions import (
    FeatureDoesNotExistError,
    FeatureUpdateError,
    FeatureRepositoryError,
)
from src.apps.feature.interactors.base_interactor import BaseInteractor


class UpdateFeatureInteractor(BaseInteractor):
    async def execute(self, dto: FeatureUpdateDTO) -> None:
        feature = await self._repository.get_entity(feature_id=dto.id)
        if not feature:
            raise FeatureDoesNotExistError(dto.id)

        try:
            feature.update_fields(dto.updated_fields)
        except ValueError as e:
            raise FeatureUpdateError(context=e) from None

        try:
            await self._repository.update(feature=feature)
        except FeatureRepositoryError as e:
            raise FeatureUpdateError(context=e) from None
