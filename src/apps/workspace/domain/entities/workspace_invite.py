from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from enum import Enum
from uuid import (
    UUID,
    uuid4,
)

from src.apps.workspace.domain.value_objects import (
    InviteID,
    WorkspaceID,
)


class StatusInvite(Enum):
    ACTIVE = "Активна"
    USED = "Использована"
    EXPIRED = "Истекла"


@dataclass
class WorkspaceInvite:
    EXPIRATION_DAYS = 7

    id_: InviteID
    workspace_id: WorkspaceID
    code: UUID = field(default_factory=uuid4)
    _status: StatusInvite = field(default=StatusInvite.ACTIVE)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    expired_at: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.expired_at = self._calculate_expired_at(self.created_at)

    def _calculate_expired_at(self, created_at: datetime) -> datetime:
        return created_at + timedelta(days=self.EXPIRATION_DAYS)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expired_at

    def change_status(self, new_status: StatusInvite) -> None:
        self._validate_status_change(new_status)
        self._status = new_status

    def change_status_to_expired(self) -> None:
        if self.is_expired():
            self._status = StatusInvite.EXPIRED

    def _validate_status_change(self, new_status: StatusInvite) -> None:
        if new_status not in StatusInvite:
            raise ValueError(f"Такого статуса нет: {new_status}")
        if new_status == self._status:
            raise ValueError('Статус уже установлен')

    @property
    def status(self) -> StatusInvite:
        return self._status
