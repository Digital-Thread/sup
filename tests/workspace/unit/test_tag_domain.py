import pytest

from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from tests.fixtures.workspace_fixtures import workspace_id


@pytest.fixture()
def tag_minimal(workspace_id: WorkspaceId) -> TagEntity:
    return TagEntity(
        _workspace_id=workspace_id,
        _name='Minimal Tag',
        _color='#FAFAFA',
    )


@pytest.fixture()
def tag_full(workspace_id: WorkspaceId) -> TagEntity:
    return TagEntity(_workspace_id=workspace_id, _name='Full Tag', _color='#FAFAFA', _id=TagId(1))


class TestTagCreation:

    def test_tag_creation_with_required_data(
        self, tag_minimal: TagEntity, workspace_id: WorkspaceId
    ) -> None:
        assert tag_minimal.name == 'Minimal Tag'
        assert tag_minimal.color == '#FAFAFA'
        assert tag_minimal._id is None
        assert tag_minimal._workspace_id == workspace_id

    def test_tag_creation_with_full_data(
        self, tag_full: TagEntity, workspace_id: WorkspaceId
    ) -> None:
        assert tag_full.name == 'Full Tag'
        assert tag_full.color == '#FAFAFA'
        assert tag_full._id == 1
        assert tag_full._workspace_id == workspace_id

    def test_tag_creation_missing_required_fields(self) -> None:
        with pytest.raises(TypeError):
            TagEntity()


class TestTagValidation:

    @pytest.mark.parametrize('name', ['Backend', 'frontend', 'PM'])
    def test_valid_tag_name(self, tag_minimal: TagEntity, name: str) -> None:
        tag_minimal.name = name
        assert tag_minimal.name == name

    @pytest.mark.parametrize('color', ['#A0A0A0', '#ffffff', '#000000'])
    def test_valid_tag_color(self, tag_minimal: TagEntity, color: str) -> None:
        tag_minimal.color = color
        assert tag_minimal.color == color

    @pytest.mark.parametrize(
        'name, expected_error_message',
        [
            ('', 'Имя Тега должно содержать хотя бы одну букву'),
            (' ', 'Имя Тега должно содержать хотя бы одну букву'),
            ('Invalid Tag@#$%&*()', 'Неверный формат названия Тега'),
            ('r' * 21, 'Длина названия Тега не должна превышать 20 символов включая пробелы'),
        ],
    )
    def test_invalid_tag_name(
        self, tag_minimal: TagEntity, name: str, expected_error_message: str
    ) -> None:
        with pytest.raises(ValueError, match=expected_error_message):
            tag_minimal.name = name

    @pytest.mark.parametrize('color', ['', ' ', '#-%&*()+', '000000', 'FAFAFA'])
    def test_invalid_tag_color(self, tag_minimal: TagEntity, color: str) -> None:
        with pytest.raises(ValueError, match=f'Неверный формат цвета {color}'):
            tag_minimal.color = color

    def test_tag_id_set_once_only(self, tag_full) -> None:
        with pytest.raises(AttributeError, match='Идентификатор тега уже установлен'):
            tag_full.id = 2
