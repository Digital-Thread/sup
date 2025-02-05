from asyncpg import ForeignKeyViolationError
from sqlalchemy import Select, delete, func, literal, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.feature import (
    FeatureAttrsWithWorkspace,
    FeatureInWorkspaceOutputDTO,
    FeatureListQuery,
    FeatureOutputDTO,
    IFeatureRepository,
)
from src.apps.feature.domain import FeatureEntity, FeatureId, WorkspaceId
from src.apps.feature.exceptions import FeatureRepositoryError
from src.data_access.mappers.feature_mapper import FeatureMapper
from src.data_access.models import (
    FeatureModel,
    ProjectModel,
    TagModel,
    UserModel,
    WorkspaceMemberModel,
)
from src.data_access.models.feature import Priority, Status


class FeatureRepository(IFeatureRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = FeatureModel
        self.mapper = FeatureMapper()

    async def _get_m2m_objects[M, ID](self, list_ids: list[ID] | None, model: type[M]) -> list[M]:
        if list_ids:
            query = select(model).where(model.id.in_(list_ids))
            result = await self._session.execute(query)
            m2m_objects = result.scalars().all()
            return list(m2m_objects)
        else:
            return []

    async def get_model(self, feature_id: FeatureId) -> FeatureModel | None:
        stmt = (
            select(self.model)
            .where(self.model.id == feature_id)
            .options(
                selectinload(self.model.tags),
                selectinload(self.model.members),
                selectinload(self.model.project),
                selectinload(self.model.owner),
                selectinload(self.model.assigned_to),
            )
        )
        result = await self._session.execute(stmt)
        feature_model = result.scalar_one_or_none()

        return feature_model

    async def get_entity(self, feature_id: FeatureId) -> FeatureEntity | None:
        feature_model = await self.get_model(feature_id=feature_id)
        if feature_model:
            return self.mapper.map_model_to_entity(feature_model=feature_model)
        return None

    async def save(self, feature: FeatureEntity) -> None:
        feature_model = await self.mapper.map_entity_to_model(feature)
        feature_model.tags = await self._get_m2m_objects(feature.tags, TagModel)
        feature_model.members = await self._get_m2m_objects(feature.members, UserModel)

        try:
            self._session.add(feature_model)
            await self._session.flush()
        except IntegrityError as e:
            orig_exception = e.orig.__cause__
            if isinstance(orig_exception, ForeignKeyViolationError):
                detail_message = orig_exception.detail
                raise FeatureRepositoryError(detail_message)
            else:
                raise

    async def get_by_id(self, feature_id: FeatureId) -> FeatureOutputDTO | None:
        feature_model = await self.get_model(feature_id=feature_id)
        if feature_model:
            return self.mapper.map_model_to_dto(feature_model=feature_model)

        return None

    async def update(self, feature: FeatureEntity) -> None:
        feature_model = await self.get_model(feature_id=feature.id)
        if feature_model:
            feature_model.name = feature.name
            feature_model.created_at = feature.created_at
            feature_model.updated_at = feature.updated_at
            feature_model.description = feature.description
            feature_model.priority = Priority[feature.priority.name]
            feature_model.status = Status[feature.status.name]
            feature_model.tags = await self._get_m2m_objects(feature.tags, TagModel)
            feature_model.members = await self._get_m2m_objects(feature.members, UserModel)
            try:
                feature_model.project_id = feature.project_id
                feature_model.assigned_to_id = feature.assigned_to
                await self._session.flush()
            except IntegrityError as e:
                orig_exception = e.orig.__cause__
                if isinstance(orig_exception, ForeignKeyViolationError):
                    detail_message = orig_exception.detail
                    raise FeatureRepositoryError(detail_message)
                else:
                    raise

    async def delete(self, feature_id: FeatureId) -> None:
        stmt = delete(self.model).where(self.model.id == feature_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise FeatureRepositoryError(message=f'Не найдена фича с id: {feature_id}')

    async def get_by_workspace_id(
        self,
        workspace_id: WorkspaceId,
        query: FeatureListQuery,
    ) -> list[FeatureInWorkspaceOutputDTO] | None:
        conditions = [self.model.workspace_id == workspace_id]

        filters = query.filters
        if filters:
            if 'members' in filters:
                conditions.append(self.model.members.any(UserModel.id.in_(filters['members'])))

            if 'tags' in filters:
                conditions.append(self.model.tags.any(TagModel.id.in_(filters['tags'])))

            if 'status' in filters:
                statuses = [Status[status.name].value for status in filters['status']]
                conditions.append(self.model.status.in_(statuses))

            if 'project' in filters:
                conditions.append(self.model.project_id.in_(filters['project']))

        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.tags),
                selectinload(self.model.members),
                selectinload(self.model.project),
            )
            .where(*conditions)
            .order_by(
                getattr(self.model, str(query.order_by.field.value)).asc()
                if query.order_by.order.value == 'ASC'
                else getattr(self.model, str(query.order_by.field.value)).desc()
            )
            .limit(query.paginate_by.limit_by)
            .offset(query.paginate_by.offset)
        )

        result = await self._session.execute(stmt)
        features = result.scalars().all()
        return (
            [self.mapper.map_model_to_workspace_dto(feature_model=f) for f in features]
            if features
            else None
        )

    def _make_stmt_for_validation(
        self,
        attrs: FeatureAttrsWithWorkspace,
    ) -> 'Select':
        project_subq = (
            select(func.count())
            .select_from(ProjectModel)
            .where(
                ProjectModel.id == attrs['project_id'],
                ProjectModel.workspace_id == attrs['workspace_id'],
            )
            .scalar_subquery()
        )

        owner_subq = (
            select(func.count())
            .select_from(WorkspaceMemberModel)
            .where(
                WorkspaceMemberModel.user_id == attrs['owner_id'],
                WorkspaceMemberModel.workspace_id == attrs['workspace_id'],
            )
            .scalar_subquery()
        )

        assigned_subq = (
            select(func.count())
            .select_from(WorkspaceMemberModel)
            .where(
                WorkspaceMemberModel.user_id == attrs['assigned_to'],
                WorkspaceMemberModel.workspace_id == attrs['workspace_id'],
            )
            .scalar_subquery()
            if attrs['assigned_to']
            else literal(0)
        )

        tag_subq = (
            select(func.count())
            .select_from(TagModel)
            .where(
                TagModel.id.in_(attrs['tags']),
                TagModel.workspace_id == attrs['workspace_id'],
            )
            .scalar_subquery()
            if attrs['tags']
            else literal(0)
        )

        member_subq = (
            select(func.count())
            .select_from(WorkspaceMemberModel)
            .where(
                WorkspaceMemberModel.user_id.in_(attrs['members']),
                WorkspaceMemberModel.workspace_id == attrs['workspace_id'],
            )
            .scalar_subquery()
            if attrs['members']
            else literal(0)
        )

        stmt = select(
            project_subq.label('cnt_project'),
            owner_subq.label('cnt_owner'),
            assigned_subq.label('cnt_assigned'),
            tag_subq.label('cnt_tags'),
            member_subq.label('cnt_members'),
        )

        return stmt

    async def validate_workspace_consistency(
        self,
        attrs: FeatureAttrsWithWorkspace,
    ) -> None:
        """
        Проверяет, что:
          - проект с id = attrs["project_id"] принадлежит workspace с id = attrs["workspace_id"],
          - владелец (owner_id) является участником workspace,
          - назначенный пользователь (assigned_to) является участником workspace,
          - все переданные теги принадлежат workspace,
          - все участники (members) числятся в workspace.

        Если хоть одна проверка не проходит, выбрасывается FeatureRepositoryError.
        """
        stmt = self._make_stmt_for_validation(attrs=attrs)
        result = await self._session.execute(stmt)
        row = result.first()

        if row is None:
            raise FeatureRepositoryError(message='Ошибка при проверке целостности workspace.')

        if row.cnt_project != 1:
            raise FeatureRepositoryError(message='Проект не принадлежит указанному workspace.')

        if row.cnt_owner != 1:
            raise FeatureRepositoryError(
                message='Владелец не является участником указанного workspace.'
            )

        if attrs['assigned_to'] and row.cnt_assigned != 1:
            raise FeatureRepositoryError(
                message='Пользователь, назначенный на выполнение, не является участником указанного workspace.'
            )

        if attrs['tags'] and row.cnt_tags != len(attrs['tags']):
            raise FeatureRepositoryError(
                message='Один или несколько тегов не принадлежат указанному workspace.'
            )

        if attrs['members'] and row.cnt_members != len(attrs['members']):
            raise FeatureRepositoryError(
                message='Один или несколько участников не состоят в указанном workspace.'
            )
