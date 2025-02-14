from asyncpg import ForeignKeyViolationError
from sqlalchemy import select, Select, func, literal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data_access.models import FeatureModel, WorkspaceMemberModel
from src.data_access.models.task import Priority, Status
from src.apps.task.domain import FeatureId, TagId, TaskEntity, TaskId
from src.apps.task import (
    ITaskRepository,
    TaskListQuery,
    TaskOutputDTO,
    TaskInFeatureOutputDTO,
    TaskRepositoryError,
    TaskAttrsWithWorkspace,
)
from src.data_access.mappers.task_mapper import TaskMapper
from src.data_access.models import TagModel, TaskModel


class TaskRepository(ITaskRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = TaskModel
        self.mapper = TaskMapper()

    async def _get_tags(
            self,
            list_ids: list[TagId] | None,
    ) -> list[TagModel]:
        if list_ids:
            query = select(TagModel).where(TagModel.id.in_(list_ids))
            result = await self._session.execute(query)
            tags = result.scalars().all()
            return list(tags)
        else:
            return []

    async def get_model(self, task_id: TaskId) -> TaskModel | None:
        stmt = (
            select(self.model)
            .where(self.model.id == task_id)
            .options(
                selectinload(self.model.tags),
                selectinload(self.model.feature),
                selectinload(self.model.owner),
                selectinload(self.model.assigned_to),
            )
        )
        result = await self._session.execute(stmt)
        task_model = result.scalar_one_or_none()

        return task_model

    async def save(self, task: TaskEntity) -> None:
        task_model = await self.mapper.map_entity_to_model(task)
        task_model.tags = await self._get_tags(task.tags)

        try:
            self._session.add(task_model)
            await self._session.flush()
        except IntegrityError as e:
            orig_exception = e.orig.__cause__
            if isinstance(orig_exception, ForeignKeyViolationError):
                detail_message = orig_exception.detail
                raise TaskRepositoryError(detail_message)
            else:
                raise

    async def get_entity(self, task_id: TaskId) -> TaskEntity | None:
        task_model = await self.get_model(task_id=task_id)
        if task_model:
            return self.mapper.map_model_to_entity(task_model=task_model)
        return None

    async def get_by_id(self, task_id: TaskId) -> TaskOutputDTO | None:
        task_model = await self.get_model(task_id=task_id)
        if task_model:
            return self.mapper.map_model_to_dto(task_model)
        else:
            return None

    async def update(self, task_id: TaskId, task: TaskEntity) -> None:
        task_model = await self.get_model(task_id=task_id)
        if task_model:
            task_model.name = task.name
            task_model.created_at = task.created_at
            task_model.updated_at = task.updated_at
            task_model.due_date = task.due_date
            task_model.description = task.description
            task_model.priority = Priority[task.priority.name]
            task_model.status = Status[task.status.name]
            task_model.tags = await self._get_tags(task.tags)
            try:
                task_model.feature_id = task.feature_id
                task_model.assigned_to_id = task.assigned_to
                await self._session.flush()
            except IntegrityError as e:
                orig_exception = e.orig.__cause__
                if isinstance(orig_exception, ForeignKeyViolationError):
                    detail_message = orig_exception.detail
                    raise TaskRepositoryError(detail_message)
                else:
                    raise

    async def delete(self, task_id: TaskId) -> None:
        task_model = await self._session.get(self.model, task_id)
        if task_model:
            await self._session.delete(task_model)
        else:
            raise TaskRepositoryError(message=f'Не найдена задача с id: {task_id}')

    async def get_by_feature_id(
            self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[TaskInFeatureOutputDTO] | None:

        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.tags),
                selectinload(self.model.assigned_to),
            )
            .where(self.model.feature_id == feature_id)
            .order_by(
                getattr(self.model, str(query.order_by.field.value)).asc()
                if query.order_by.order.value == 'ASC'
                else getattr(self.model, str(query.order_by.field.value)).desc()
            )
            .limit(query.paginate_by.limit_by)
            .offset(query.paginate_by.offset)
        )

        result = await self._session.execute(stmt)
        tasks = result.scalars().all()
        return (
            [self.mapper.map_model_to_for_feature_dto(t) for t in tasks]
            if tasks
            else None
        )

    def _make_stmt_for_validation(
            self,
            attrs: TaskAttrsWithWorkspace,
    ) -> 'Select':
        feature_subq = (
            select(func.count())
            .select_from(FeatureModel)
            .where(
                FeatureModel.id == attrs['feature_id'],
                FeatureModel.workspace_id == attrs['workspace_id'],
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

        stmt = select(
            feature_subq.label('cnt_feature'),
            owner_subq.label('cnt_owner'),
            assigned_subq.label('cnt_assigned'),
            tag_subq.label('cnt_tags'),
        )

        return stmt

    async def validate_workspace_consistency(
            self,
            attrs: TaskAttrsWithWorkspace,
    ) -> None:
        """
        Проверяет, что:
          - фича с id = attrs["feature_id"] принадлежит workspace с id = attrs["workspace_id"],
          - владелец (owner_id) является участником workspace,
          - назначенный пользователь (assigned_to) является участником workspace,
          - все переданные теги принадлежат workspace,

        Если хоть одна проверка не проходит, выбрасывается TaskRepositoryError.
        """
        stmt = self._make_stmt_for_validation(attrs=attrs)
        result = await self._session.execute(stmt)
        row = result.first()

        if row is None:
            raise TaskRepositoryError(message='Ошибка при проверке целостности workspace.')

        if row.cnt_feature != 1:
            raise TaskRepositoryError(message='Фича не принадлежит указанному workspace.')

        if row.cnt_owner != 1:
            raise TaskRepositoryError(
                message='Владелец не является участником указанного workspace.'
            )

        if row.cnt_assigned != 1:
            raise TaskRepositoryError(
                message='Пользователь, назначенный на выполнение, не является участником указанного workspace.'
            )

        if attrs['tags'] and row.cnt_tags != len(attrs['tags']):
            raise TaskRepositoryError(
                message='Один или несколько тегов не принадлежат указанному workspace.'
            )
