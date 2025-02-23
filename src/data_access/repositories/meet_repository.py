from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.meet import IMeetRepository, MeetListQuery
from src.apps.meet.domain import MeetEntity, MeetId
from src.apps.meet.exceptions import MeetRepositoryError
from src.data_access.mappers import MeetMapper
from src.data_access.models import MeetModel
from src.providers.context import WorkspaceContext


class MeetRepository(IMeetRepository):
    def __init__(self, session: AsyncSession, context: WorkspaceContext):
        self._session = session
        self.model = MeetModel
        self.converter = MeetMapper()
        self._context = context

    def _base_select(self) -> Select:
        return select(self.model).where(self.model.workspace_id == self._context.workspace_id)

    def _get_meet_by_id(self, meet_id: MeetId) -> Select:
        return self._base_select().where(self.model.id == meet_id)

    async def save(self, meet: MeetEntity) -> MeetId:
        meet_model = self.converter.map_entity_to_model(meet)

        try:
            self._session.add(meet_model)
            await self._session.flush()
            return MeetId(meet_model.id)
        except SQLAlchemyError as e:
            raise MeetRepositoryError(context=e) from e

    async def get_by_id(self, meet_id: MeetId) -> MeetEntity:
        stmt = self._get_meet_by_id(meet_id).options(
            selectinload(self.model.participants),
        )
        result = await self._session.execute(stmt)
        meet_model = result.scalar_one_or_none()
        if meet_model:
            return self.converter.map_model_to_entity(meet_model=meet_model)

        raise MeetRepositoryError(message=f'Not found meet with id: {meet_id}')

    async def get_list(
        self,
        query: MeetListQuery,
    ) -> list[MeetEntity]:
        conditions = []
        if query.filters:
            for key, value in query.filters.items():
                column_ = getattr(self.model, key, None)
                if column_:
                    conditions.append(column_ == value)

        stmt = (
            select(self.model)
            .options(selectinload(self.model.participants))
            .where(
                self.model.workspace_id == self._context.workspace_id,
                *conditions,
            )
            .order_by(
                getattr(self.model, str(query.order_by.field.value)).asc()
                if query.order_by.order.value == 'ASC'
                else getattr(self.model, str(query.order_by.field.value)).desc()
            )
            .limit(query.paginate_by.limit_by)
            .offset(query.paginate_by.offset)
        )

        result = await self._session.execute(stmt)
        meets = result.scalars().all()
        return [self.converter.map_model_to_entity(meet_model=m) for m in meets]

    async def update(self, meet: MeetEntity) -> None:
        stmt = self._get_meet_by_id(meet.id)
        result = await self._session.execute(stmt)
        meet_model = result.scalar_one_or_none()
        if meet_model:
            meet_model.name = meet.name
            meet_model.meet_at = meet.meet_at
            meet_model.category_id = meet.category_id
            meet_model.assigned_to_id = meet.assigned_to
            meet_model.workspace_id = meet.workspace_id
            meet_model.created_at = meet.created_at
            meet_model.updated_at = meet.updated_at
            try:
                await self._session.flush()
            except SQLAlchemyError as e:
                raise MeetRepositoryError(context=e) from e

    async def delete(self, meet_id: MeetId) -> None:
        stmt = self._get_meet_by_id(meet_id)
        result = await self._session.execute(stmt)
        meet_model = result.scalar_one_or_none()
        if meet_model:
            await self._session.delete(meet_model)
        else:
            raise MeetRepositoryError(message=f'Not found meet with id: {meet_id}')
