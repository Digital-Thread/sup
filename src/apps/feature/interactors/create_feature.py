from src.apps.feature.mapper import FeatureMapper
from src.apps.feature.dtos import FeatureInputDTO
from src.apps.feature.exceptions import FeatureCreateError, FeatureRepositoryError
from src.apps.feature.interactors.base_interactor import BaseInteractor


class CreateFeatureInteractor(BaseInteractor):
    async def execute(self, dto: FeatureInputDTO) -> None:
        try:
            feature = FeatureMapper.dto_to_entity(dto=dto)
        except (ValueError, AttributeError) as e:
            raise FeatureCreateError(context=e) from None

        try:
            await self._repository.save(feature=feature)
        except FeatureRepositoryError as e:
            raise FeatureCreateError(context=e) from None
