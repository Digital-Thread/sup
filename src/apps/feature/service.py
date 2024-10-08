from apps.feature.domain.entities.feature import Feature
from apps.feature.domain.value_objects import FeatureId
from apps.feature.dtos import FeatureInputDTO, FeatureUpdateDTO
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

    async def get_feature_by_id(self, feature_id: FeatureId) -> Feature:
        feature = await self._repository.get_by_id(feature_id=feature_id)
        if not feature:
            raise FeatureDoesNotExistError(feature_id)
        return feature

    async def update_feature(self, dto: FeatureUpdateDTO) -> None:
        feature = await self._repository.get_by_id(feature_id=dto.id)
        if not feature:
            raise FeatureDoesNotExistError(dto.id)
        try:
            for field, value in dto.updated_fields.items():
                setattr(feature, field, value)

        except ValueError as e:
            raise FeatureUpdateError(context=e) from None

        feature.mark_as_updated()
        await self._repository.update(feature)

    async def delete_feature(self, feature_id: FeatureId) -> None:
        feature = await self._repository.get_by_id(feature_id=feature_id)
        if not feature:
            raise FeatureDoesNotExistError(feature_id)
        await self._repository.delete(feature_id=feature_id)

    async def get_feature_list(self, query: FeatureListQuery) -> list[Feature]:
        return await self._repository.get_list(query=query)
