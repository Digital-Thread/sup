from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.apps.meet.domain import (
    MeetId,
    ParticipantId,
    Status,
    UserId,
)


class CreateParticipantRequestDTO(BaseModel):
    meet_id: MeetId
    user_id: UserId
    status: Status = Status.UNDEFINED


class UpdateParticipantRequestDTO(BaseModel):
    status: Status | None = None


class ParticipantResponseDTO(BaseModel):
    id: ParticipantId
    meet_id: MeetId
    user_id: UserId
    status: Status
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )
