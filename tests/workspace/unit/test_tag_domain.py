from uuid import uuid4

import pytest

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId

WORKSPACE_ID = uuid4()


@pytest.fixture()
def tag_minimal():
    return Tag(
        _workspace_id=WorkspaceId(WORKSPACE_ID),
        _name='Minimal Tag',
        _color='#FAFAFA',
    )


@pytest.fixture()
def tag_full():
    return Tag(
        _workspace_id=WorkspaceId(WORKSPACE_ID), _name='Full Tag', _color='#FAFAFA', _id=TagId(1)
    )


class TestTagCreation:

    def test_tag_creation_with_required_data(self, tag_minimal):
        assert tag_minimal.name == 'Minimal Tag'
        assert tag_minimal.color == '#FAFAFA'
        assert tag_minimal._id is None
        assert tag_minimal._workspace_id == WORKSPACE_ID

    def test_tag_creation_with_full_data(self, tag_full):
        assert tag_full.name == 'Full Tag'
        assert tag_full.color == '#FAFAFA'
        assert tag_full._id == 1
        assert tag_full._workspace_id == WORKSPACE_ID

    def test_tag_creation_missing_required_fields(self):
        with pytest.raises(TypeError):
            Tag()


class TestTagValidation:

    @pytest.mark.parametrize('name', ['Backend', 'frontend', 'PM'])
    def test_valid_tag_name(self, tag_minimal, name):
        tag_minimal.name = name
        assert tag_minimal.name == name

    @pytest.mark.parametrize('color', ['#A0A0A0', '#ffffff', '#000000'])
    def test_valid_tag_color(self, tag_minimal, color):
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
    def test_invalid_tag_name(self, tag_minimal, name, expected_error_message):
        with pytest.raises(ValueError, match=expected_error_message):
            tag_minimal.name = name

    @pytest.mark.parametrize('color', ['', ' ', '#-%&*()+', '000000', 'FAFAFA'])
    def test_invalid_tag_color(self, tag_minimal, color):
        with pytest.raises(ValueError, match=f'Неверный формат цвета {color}'):
            tag_minimal.color = color

    def test_tag_id_set_once_only(self, tag_full):
        with pytest.raises(AttributeError, match='Идентификатор тега уже установлен'):
            tag_full.id = 2
