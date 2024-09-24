from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class StatusInvite(Enum):
    ACTIVE = 'Активна'
    USED = 'Использована'
    EXPIRED = 'Истекла'


@dataclass
class WorkspaceInvite:
    EXPIRATION_DAYS = 7

    _workspace_id: UUID
    __id: Optional[int] = field(default=None)
    __code: UUID = field(default_factory=uuid4)
    _status: StatusInvite = field(default=StatusInvite.ACTIVE)
    __created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    __expired_at: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.__expired_at = self._calculate_expired_at(self.__created_at)

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
    def id(self) -> int:
        return self.__id

    @property
    def workspace_id(self) -> UUID:
        return self._workspace_id

    @property
    def code(self) -> UUID:
        return self.__code

    @property
    def status(self) -> StatusInvite:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def expired_at(self) -> datetime:
        return self.__expired_at
