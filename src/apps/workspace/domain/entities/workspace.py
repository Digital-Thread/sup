from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Set

from src.apps.workspace.domain.value_objects import (
    CategoryID,
    OwnerID,
    RoleID,
    TagID,
    WorkspaceID,
)


@dataclass
class Workspace:
    id_: WorkspaceID
    owner_id: OwnerID
    name: str
    _category_id: Optional[CategoryID] = field(default=None)
    description: Optional[str] = field(default=None, compare=False)
    logo: Optional[str] = field(default=None, compare=False)
    _role_ids: Set[RoleID] = field(default_factory=set, compare=False)
    _tag_ids: Set[TagID] = field(default_factory=set, compare=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add_role(self, role_id: RoleID) -> None:
        if role_id < 0:
            raise ValueError('Id роли не может быть отрицательным.')
        self._role_ids.add(role_id)

    def remove_role(self, role_id: RoleID) -> None:
        if role_id not in self._role_ids:
            raise ValueError('Роль не найдена в этом рабочем пространстве.')
        self._role_ids.remove(role_id)

    def add_tag(self, tag_id: TagID) -> None:
        if tag_id < 0:
            raise ValueError('Id тега не может быть отрицательным.')
        self._tag_ids.add(tag_id)

    def remove_tag(self, tag_id: TagID) -> None:
        if tag_id not in self._tag_ids:
            raise ValueError('Тег не найден в этом рабочем пространстве')
        self._tag_ids.remove(tag_id)

    @property
    def category(self) -> CategoryID:
        return self._category_id

    @category.setter
    def category(self, category_id: CategoryID) -> None:
        if category_id < 0:
            raise ValueError(f'Id категории не может быть отрицательным.')

        self._category_id = category_id

    @property
    def roles(self) -> Set[RoleID]:
        return self._role_ids

    @property
    def tags(self) -> Set[TagID]:
        return self._tag_ids
