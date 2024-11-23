import pytest

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from tests.fixtures.workspace_fixtures import workspace_id


@pytest.fixture()
def role_minimal(workspace_id: WorkspaceId) -> RoleEntity:
    return RoleEntity(
        _workspace_id=workspace_id,
        _name='Minimal Role',
        _color='#FAFAFA',
    )


@pytest.fixture()
def role_full(workspace_id: WorkspaceId) -> RoleEntity:
    return RoleEntity(_workspace_id=workspace_id, _name='Full Role', _color='#FAFAFA', _id=RoleId(1))


class TestRoleCreation:

    def test_role_creation_with_required_data(
        self, role_minimal: RoleEntity, workspace_id: WorkspaceId
    ) -> None:
        assert role_minimal.name == 'Minimal Role'
        assert role_minimal.color == '#FAFAFA'
        assert role_minimal._id is None
        assert role_minimal._workspace_id == workspace_id

    def test_role_creation_with_full_data(self, role_full: RoleEntity, workspace_id: WorkspaceId) -> None:
        assert role_full.name == 'Full Role'
        assert role_full.color == '#FAFAFA'
        assert role_full._id == 1
        assert role_full._workspace_id == workspace_id

    def test_role_creation_missing_required_fields(self) -> None:
        with pytest.raises(TypeError):
            RoleEntity()


class TestRoleValidation:

    @pytest.mark.parametrize('name', ['Backend', 'frontend', 'PM'])
    def test_valid_role_name(self, role_minimal: RoleEntity, name: str) -> None:
        role_minimal.name = name
        assert role_minimal.name == name

    @pytest.mark.parametrize('color', ['#A0A0A0', '#ffffff', '#000000'])
    def test_valid_role_color(self, role_minimal: RoleEntity, color: str) -> None:
        role_minimal.color = color
        assert role_minimal.color == color

    @pytest.mark.parametrize(
        'name, expected_error_message',
        [
            ('', 'Имя Роли должно содержать хотя бы одну букву'),
            (' ', 'Имя Роли должно содержать хотя бы одну букву'),
            ('Invalid Role@#$%&*()', 'Неверный формат названия Роли'),
            ('r' * 21, 'Длина названия Роли не должна превышать 20 символов включая пробелы'),
        ],
    )
    def test_invalid_role_name(
        self, role_minimal: RoleEntity, name: str, expected_error_message: str
    ) -> None:
        with pytest.raises(ValueError, match=expected_error_message):
            role_minimal.name = name

    @pytest.mark.parametrize('color', ['', ' ', '#-%&*()+', '000000', 'FAFAFA'])
    def test_invalid_role_color(self, role_minimal: RoleEntity, color: str) -> None:
        with pytest.raises(ValueError, match=f'Неверный формат цвета {color}'):
            role_minimal.color = color

    def test_role_id_set_once_only(self, role_full: RoleEntity) -> None:
        with pytest.raises(AttributeError, match='Идентификатор роли уже установлен'):
            role_full.id = 2
