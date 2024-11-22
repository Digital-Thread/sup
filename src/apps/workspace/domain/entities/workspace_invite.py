from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from uuid import UUID, uuid4

from src.apps.workspace.domain.types_ids import InviteId, WorkspaceId


class StatusInvite(Enum):
    ACTIVE = 'Активна'
    USED = 'Использована'
    EXPIRED = 'Истекла'


@dataclass
class WorkspaceInviteEntity:
    EXPIRATION_DAYS = 7

    _workspace_id: WorkspaceId
    _id: InviteId | None = field(default=None)
    code: UUID = field(default_factory=uuid4)
    _status: StatusInvite = field(default=StatusInvite.ACTIVE)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _expired_at: datetime = field(init=False)

    def __post_init__(self) -> None:
        self._expired_at = self._calculate_expired_at(self.created_at)

    def _calculate_expired_at(self, created_at: datetime) -> datetime:
        return created_at + timedelta(days=self.EXPIRATION_DAYS)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc).date() >= self.expired_at.date()

    def activate(self) -> None:
        self._validate_status_change(StatusInvite.ACTIVE)
        self._status = StatusInvite.ACTIVE

    def use(self) -> None:
        self._validate_status_change(StatusInvite.USED)
        self._status = StatusInvite.USED

    def expire(self) -> None:
        if self.is_expired():
            self._status = StatusInvite.EXPIRED
        else:
            raise ValueError('Приглашение ещё не истекло')

    def _validate_status_change(self, new_status: StatusInvite) -> None:
        if new_status == self._status:
            raise ValueError('Статус уже установлен')

    @property
    def id(self) -> InviteId:
        return self._id

    @id.setter
    def id(self, new_id: InviteId) -> None:
        if self._id is not None:
            raise AttributeError('Идентификатор ссылки приглашения уже установлен')

        self._id = new_id

    @property
    def workspace_id(self) -> WorkspaceId:
        return self._workspace_id

    @property
    def status(self) -> StatusInvite:
        return self._status

    @property
    def expired_at(self) -> datetime:
        return self._expired_at
