from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.meet import IParticipantRepository
from src.apps.meet.domain import MeetId, ParticipantEntity, ParticipantId
from src.apps.meet.exceptions import MeetRepositoryError
from src.data_access.mappers import MeetParticipantConverter
from src.data_access.models import MeetModel, ParticipantModel
from src.providers.context import WorkspaceContext


class MeetParticipantRepository(IParticipantRepository):
    def __init__(self, session: AsyncSession, context: WorkspaceContext):
        self._session = session
        self._context = context
        self.model = ParticipantModel
        self.converter = MeetParticipantConverter()

    def _base_select(self) -> Select:
        return select(self.model).where(
            ParticipantModel.meet.has(MeetModel.workspace_id == self._context.workspace_id)
        )

    def _get_participant_by_id(self, participant_id: ParticipantId) -> Select:
        return self._base_select().where(self.model.id == participant_id)

    async def save(self, participant: ParticipantEntity) -> ParticipantId:
        participant_model = self.converter.map_entity_to_model(participant)

        try:
            self._session.add(participant_model)
            await self._session.flush()
            return ParticipantId(participant_model.id)
        except SQLAlchemyError as e:
            raise MeetRepositoryError(context=e) from e

    async def get_by_id(self, participant_id: ParticipantId) -> ParticipantEntity:
        stmt = self._get_participant_by_id(participant_id)
        result = await self._session.execute(stmt)
        participant_model = result.scalar_one_or_none()
        if participant_model:
            return self.converter.map_model_to_entity(participant_model=participant_model)

        raise MeetRepositoryError(message=f'Not found participant with id: {participant_id}')

    async def get_list(self, meet_id: MeetId) -> list[ParticipantEntity]:
        stmt = self._base_select().where(self.model.meet_id == meet_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self.converter.map_model_to_entity(model) for model in models]

    async def update(self, participant: ParticipantEntity) -> None:
        stmt = self._get_participant_by_id(participant.id)
        result = await self._session.execute(stmt)
        participant_model = result.scalar_one_or_none()
        if participant_model:
            participant_model.status = participant.status
            try:
                await self._session.flush()
            except SQLAlchemyError as e:
                raise MeetRepositoryError(context=e) from e

    async def delete(self, participant_id: ParticipantId) -> None:
        stmt = self._get_participant_by_id(participant_id)
        result = await self._session.execute(stmt)
        participant_model = result.scalar_one_or_none()
        if participant_model:
            await self._session.delete(participant_model)
        else:
            raise MeetRepositoryError(message=f'Not found participant with id: {participant_id}')
