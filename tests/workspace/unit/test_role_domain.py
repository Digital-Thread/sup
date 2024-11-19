from uuid import uuid4

import pytest

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId

WORKSPACE_ID = uuid4()


@pytest.fixture()
def role_minimal():
    return Role(
        _workspace_id=WorkspaceId(WORKSPACE_ID),
        _name='Minimal Role',
        _color='#FAFAFA',
    )


@pytest.fixture()
def role_full():
    return Role(
        _workspace_id=WorkspaceId(WORKSPACE_ID), _name='Full Role', _color='#FAFAFA', _id=RoleId(1)
    )


class TestRoleCreation:

    def test_role_creation_with_required_data(self, role_minimal):
        assert role_minimal.name == 'Minimal Role'
        assert role_minimal.color == '#FAFAFA'
        assert role_minimal._id is None
        assert role_minimal._workspace_id == WORKSPACE_ID

    def test_role_creation_with_full_data(self, role_full):
        assert role_full.name == 'Full Role'
        assert role_full.color == '#FAFAFA'
        assert role_full._id == 1
        assert role_full._workspace_id == WORKSPACE_ID

    def test_role_creation_missing_required_fields(self):
        with pytest.raises(TypeError):
            Role()


class TestRoleValidation:

    @pytest.mark.parametrize('name', ['Backend', 'frontend', 'PM'])
    def test_valid_role_name(self, role_minimal, name):
        role_minimal.name = name
        assert role_minimal.name == name

    @pytest.mark.parametrize('color', ['#A0A0A0', '#ffffff', '#000000'])
    def test_valid_role_color(self, role_minimal, color):
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
    def test_invalid_role_name(self, role_minimal, name, expected_error_message):
        with pytest.raises(ValueError, match=expected_error_message):
            role_minimal.name = name

    @pytest.mark.parametrize('color', ['', ' ', '#-%&*()+', '000000', 'FAFAFA'])
    def test_invalid_role_color(self, role_minimal, color):
        with pytest.raises(ValueError, match=f'Неверный формат цвета {color}'):
            role_minimal.color = color

    def test_role_id_set_once_only(self, role_full):
        with pytest.raises(AttributeError, match='Идентификатор роли уже установлен'):
            role_full.id = 2
