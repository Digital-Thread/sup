from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Priority(Enum):
    CRITICAL = (5, 'Критическая')
    HIGH = (4, 'Высокая')
    MEDIUM = (3, 'Средняя')
    LOW = (2, 'Низкая')
    NO_PRIORITY = (1, 'Не задана')

    @property
    def level(self):
        return self.value[0]

    @property
    def display(self):
        return self.value[1]


class Status(Enum):
    FINISH = (4, 'Готово')
    TEST = (3, 'Тестирование')
    DEVELOPMENT = (2, 'Разработка')
    NEW = (1, 'Новая')

    @property
    def level(self):
        return self.value[0]

    @property
    def display(self):
        return self.value[1]


@dataclass
class Feature:
    name: str
    project_id: UUID
    owner_id: UUID
    assigned_to: UUID | None = field(default=None)
    description: str | None = field(default=None)
    priority: Priority = field(default=Priority.NO_PRIORITY)
    status: Status = field(default=Status.NEW)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
