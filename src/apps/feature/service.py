from apps.feature.domain.aliases import FeatureId
from apps.feature.domain.entities.feature import Feature
from apps.feature.dtos import FeatureInputDTO, FeatureOutputDTO, FeatureUpdateDTO
from apps.feature.exceptions import (
    FeatureCreateError,
    FeatureDoesNotExistError,
    FeatureUpdateError,
)
from apps.feature.repositories.feature_repository import (
    FeatureListQuery,
    IFeatureRepository,
)


class FeatureService:

    def __init__(self, feature_repository: IFeatureRepository):
        self._repository = feature_repository

    async def create_feature(self, dto: FeatureInputDTO) -> None:
        try:
            feature = Feature(
                name=dto.name,
                project_id=dto.project_id,
                owner_id=dto.owner_id,
                assigned_to=dto.assigned_to,
                description=dto.description,
                priority=dto.priority,
                status=dto.status,
                tags=dto.tags,
                members=dto.members,
            )
        except ValueError as e:
            raise FeatureCreateError(context=e) from None
        await self._repository.create(feature=feature)

    async def get_feature_by_id(self, feature_id: FeatureId) -> FeatureOutputDTO:
        feature = await self._repository.get_by_id(feature_id=feature_id)
        if not feature:
            raise FeatureDoesNotExistError(feature_id)
        feature_dto = FeatureOutputDTO.from_entity(feature_id=feature_id, entity=feature)

        return feature_dto

    async def update_feature(self, dto: FeatureUpdateDTO) -> None:
        feature = await self._repository.get_by_id(feature_id=dto.id)
        if not feature:
            raise FeatureDoesNotExistError(dto.id)

        try:
            feature.update_fields(dto.updated_fields)
        except ValueError as e:
            raise FeatureUpdateError(context=e) from None

        await self._repository.update(feature_id=dto.id, feature=feature)

    async def delete_feature(self, feature_id: FeatureId) -> None:
        feature = await self._repository.get_by_id(feature_id=feature_id)
        if not feature:
            raise FeatureDoesNotExistError(feature_id)
        await self._repository.delete(feature_id=feature_id)

    async def get_feature_list(self, query: FeatureListQuery) -> list[FeatureOutputDTO]:
        features = await self._repository.get_list(query=query)
        output = [FeatureOutputDTO.from_entity(*feature) for feature in features]
        return output
