from asyncpg import ForeignKeyViolationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.task.domain import FeatureId, TagId, TaskEntity, TaskId
from src.apps.task.exceptions import RepositoryError
from src.apps.task import ITaskRepository, TaskListQuery
from src.data_access.mappers.task_converter import TaskConverter
from src.data_access.models import TagModel, TaskModel


class TaskRepository(ITaskRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = TaskModel
        self.converter = TaskConverter()

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
            .options(selectinload(self.model.tags))
        )
        result = await self._session.execute(stmt)
        task_model = result.scalar_one_or_none()

        return task_model

    async def save(self, task: TaskEntity) -> None:
        task_model = await self.converter.map_entity_to_model(task)
        task_model.tags = await self._get_tags(task.tags)

        try:
            self._session.add(task_model)
            await self._session.flush()
        except IntegrityError as e:
            orig_exception = e.orig.__cause__
            if isinstance(orig_exception, ForeignKeyViolationError):
                detail_message = orig_exception.detail
                raise RepositoryError(detail_message)
            else:
                raise

    async def get_by_id(self, task_id: TaskId) -> TaskEntity | None:
        task_model = await self.get_model(task_id=task_id)
        if task_model:
            return self.converter.map_model_to_entity(task_model)
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
            task_model.priority = task.priority
            task_model.status = task.status
            task_model.tags = await self._get_tags(task.tags)
            try:
                task_model.feature_id = task.feature_id
                task_model.assigned_to_id = task.assigned_to
                await self._session.flush()
            except IntegrityError as e:
                orig_exception = e.orig.__cause__
                if isinstance(orig_exception, ForeignKeyViolationError):
                    detail_message = orig_exception.detail
                    raise RepositoryError(detail_message)
                else:
                    raise

    async def delete(self, task_id: TaskId) -> None:
        task_model = await self._session.get(self.model, task_id)
        if task_model:
            await self._session.delete(task_model)
        else:
            raise RepositoryError(message=f'Не найдена задача с id: {task_id}')

    async def get_list(
            self, feature_id: FeatureId, query: TaskListQuery
    ) -> list[tuple[TaskId, TaskEntity]] | None:

        stmt = (
            select(self.model)
            .options(selectinload(self.model.tags))
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
            [(TaskId(t.id), self.converter.map_model_to_entity(t)) for t in tasks]
            if tasks
            else None
        )
