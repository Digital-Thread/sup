from asyncpg import ForeignKeyViolationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.feature.domain import Feature, FeatureId, TagId, UserId, WorkspaceId
from src.apps.feature.exceptions import RepositoryError
from src.apps.feature.repositories import FeatureListQuery, IFeatureRepository
from src.data_access.models import FeatureModel, TagModel, UserModel
from src.data_access.repositories.feature.mapper import FeatureMapper


class FeatureRepository(IFeatureRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = FeatureModel
        self.mapper = FeatureMapper()

    async def _get_m2m_objects(
        self, list_ids: list[TagId | UserId] | None, model: TagModel | UserModel
    ) -> list[TagModel | UserModel] | None:
        if list_ids:
            query = select(model).where(model.id.in_(list_ids))
            result = await self._session.execute(query)
            m2m_objects = result.scalars().all()
            return list(m2m_objects)
        else:
            return None

    async def save(self, feature: Feature) -> None:
        feature_model = self.mapper.map_entity_to_model(feature)
        feature_model.tags = await self._get_m2m_objects(feature.tags, TagModel)
        feature_model.members = await self._get_m2m_objects(feature.members, UserModel)

        try:
            self._session.add(feature_model)
            await self._session.flush()
        except IntegrityError as e:
            orig_exception = e.orig.__cause__
            if isinstance(orig_exception, ForeignKeyViolationError):
                detail_message = orig_exception.detail
                raise RepositoryError(detail_message)
            else:
                raise

    async def get_by_id(self, feature_id: FeatureId) -> Feature | None:
        stmt = (
            select(self.model)
            .where(self.model.id == feature_id)
            .options(selectinload(self.model.tags), selectinload(self.model.members))
        )
        result = await self._session.execute(stmt)
        feature_model = result.scalar_one_or_none()
        if feature_model:
            return self.mapper.map_model_to_entity(feature_model)
        else:
            return None

    async def update(self, feature_id: FeatureId, feature: Feature) -> None:
        feature_model = await self.get_by_id(feature_id=feature_id)
        if feature_model:
            feature_model.name = feature.name
            feature_model.created_at = feature.created_at
            feature_model.updated_at = feature.updated_at
            feature_model.description = feature.description
            feature_model.priority = feature.priority
            feature_model.status = feature.status
            feature_model.tags = await self._get_m2m_objects(feature.tags, TagModel)
            feature_model.members = await self._get_m2m_objects(feature.members, UserModel)

            try:
                feature_model.project_id = feature.project_id
                feature_model.assigned_to = feature.assigned_to
                await self._session.flush()
            except IntegrityError as e:
                orig_exception = e.orig.__cause__
                if isinstance(orig_exception, ForeignKeyViolationError):
                    detail_message = orig_exception.detail
                    raise RepositoryError(detail_message)
                else:
                    raise

    async def delete(self, feature_id: FeatureId) -> None:
        feature_model = await self._session.get(self.model, feature_id)
        if feature_model:
            await self._session.delete(feature_model)
        else:
            raise RepositoryError(message=f'Не найдена фича с id: {feature_id}')

    async def get_list(
        self, workspace_id: WorkspaceId, query: FeatureListQuery
    ) -> list[tuple[FeatureId, Feature]] | None:
        filters = {k: v for k, v in (query.filters or {}).items() if v is not None}
        stmt = (
            select(self.model)
            .options(selectinload(self.model.tags), selectinload(self.model.members))
            .filter_by(workspace_id=workspace_id, **filters)
            .order_by(
                getattr(self.model, str(query.order_by.field)).asc()
                if query.order_by.order == 'ASC'
                else getattr(self.model, str(query.order_by.field)).desc()
            )
            .limit(query.paginate_by.limit_by)
            .offset(query.paginate_by.offset)
        )
        result = await self._session.execute(stmt)
        features = result.scalars().all()
        return [self.mapper.map_model_to_entity(f) for f in features] if features else None
