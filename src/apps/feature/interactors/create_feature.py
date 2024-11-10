from src.apps.feature import FeatureInputDTO
from src.apps.feature.domain import Feature
from src.apps.feature.exceptions import FeatureCreateError, RepositoryError
from src.apps.feature.interactors.base_interactor import BaseInteractor


class CreateFeatureInteractor(BaseInteractor):
    async def execute(self, dto: FeatureInputDTO) -> None:
        try:
            feature = Feature(
                workspace_id=dto.workspace_id,
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

        try:
            await self._repository.save(feature=feature)
        except RepositoryError as e:
            raise FeatureCreateError(context=e) from None
