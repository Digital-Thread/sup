from uuid import uuid4

import pytest

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId

WORKSPACE_ID = uuid4()


@pytest.fixture()
def category_minimal():
    return Category(
        _workspace_id=WorkspaceId(WORKSPACE_ID),
        _name='Minimal Category',
    )


@pytest.fixture()
def category_full():
    return Category(
        _workspace_id=WorkspaceId(WORKSPACE_ID), _name='Full Category', _id=CategoryId(1)
    )


class TestCategoryCreation:

    def test_category_creation_with_required_data(self, category_minimal):
        assert category_minimal.name == 'Minimal Category'
        assert category_minimal._id is None
        assert category_minimal._workspace_id == WORKSPACE_ID

    def test_category_creation_with_full_data(self, category_full):
        assert category_full.name == 'Full Category'
        assert category_full._id == 1
        assert category_full._workspace_id == WORKSPACE_ID

    def test_category_creation_missing_required_fields(self):
        with pytest.raises(TypeError):
            Category()


class TestCategoryValidation:

    @pytest.mark.parametrize('name', ['Backend', 'frontend', 'PM'])
    def test_valid_category_name(self, category_minimal, name):
        category_minimal.name = name
        assert category_minimal.name == name

    @pytest.mark.parametrize(
        'name, expected_error_message',
        [
            ('', 'Имя Категории должно содержать хотя бы одну букву'),
            (' ', 'Имя Категории должно содержать хотя бы одну букву'),
            ('Invalid @#$%&*()', 'Неверный формат названия Категории'),
            ('r' * 22, 'Длина названия Категории не должна превышать 20 символов включая пробелы'),
        ],
    )
    def test_invalid_category_name(self, category_minimal, name, expected_error_message):
        with pytest.raises(ValueError, match=expected_error_message):
            category_minimal.name = name

    def test_category_id_set_once_only(self, category_full):
        with pytest.raises(AttributeError, match='Идентификатор категории уже установлен'):
            category_full.id = 2
