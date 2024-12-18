from dataclasses import dataclass, field

from src.apps.workspace.domain.validator_mixins import NameValidatorMixin
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId


@dataclass
class CategoryEntity(NameValidatorMixin):
    _name: str
    _workspace_id: WorkspaceId | None = field(default=None)
    _id: CategoryId | None = field(default=None)

    def __post_init__(self) -> None:
        self._is_valid_name(self._name, 'Категории')

    @property
    def id(self) -> CategoryId | None:
        return self._id

    @id.setter
    def id(self, new_id: CategoryId) -> None:
        if self._id is not None:
            raise AttributeError('Идентификатор категории уже установлен')

        self._id = new_id

    @property
    def workspace_id(self) -> WorkspaceId:
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, new_workspace_id: WorkspaceId) -> None:
        if self._workspace_id is not None:
            raise AttributeError('Идентификатор рабочего пространства уже установлен')

        self._workspace_id = new_workspace_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._is_valid_name(new_name, 'Категории')
        self._name = new_name
