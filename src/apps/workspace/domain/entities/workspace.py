from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)
from typing import (
    List,
    Optional,
)

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
    category_id: Optional[CategoryID] = field(default=None)
    description: Optional[str] = field(default=None, compare=False)
    logo: Optional[str] = field(default=None, compare=False)
    _role_ids: List[RoleID] = field(default_factory=list, compare=False)
    _tag_ids: List[TagID] = field(default_factory=list, compare=False)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_role(self, role_id: RoleID) -> None:
        if role_id >= 0:
            self._role_ids.append(role_id)

    def remove_role(self, role_id: RoleID) -> None:
        self._role_ids.remove(role_id)

    def add_tag(self, tag_id: TagID) -> None:
        if tag_id >= 0:
            self._tag_ids.append(tag_id)

    def remove_tag(self, tag_id: TagID) -> None:
        self._tag_ids.remove(tag_id)

    @property
    def roles(self):
        return self._role_ids

    @property
    def tags(self):
        return self._tag_ids

workspace = Workspace(id_=WorkspaceID(1), owner_id=OwnerID(1), name='WorkspaceOleg')
print(workspace)