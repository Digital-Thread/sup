import pytest

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import CategoryId
from tests.fixtures.workspace_fixtures import workspace_id


@pytest.fixture()
def category_minimal(workspace_id) -> Category:
    return Category(
        _workspace_id=workspace_id,
        _name='Minimal Category',
    )


@pytest.fixture()
def category_full(workspace_id) -> Category:
    return Category(_workspace_id=workspace_id, _name='Full Category', _id=CategoryId(1))


class TestCategoryCreation:

    def test_category_creation_with_required_data(
        self, category_minimal: Category, workspace_id
    ) -> None:
        assert category_minimal.name == 'Minimal Category'
        assert category_minimal._id is None
        assert category_minimal._workspace_id == workspace_id

    def test_category_creation_with_full_data(self, category_full: Category, workspace_id) -> None:
        assert category_full.name == 'Full Category'
        assert category_full._id == 1
        assert category_full._workspace_id == workspace_id

    def test_category_creation_missing_required_fields(self) -> None:
        with pytest.raises(TypeError):
            Category()


class TestCategoryValidation:

    @pytest.mark.parametrize('name', ['Backend', 'frontend', 'PM'])
    def test_valid_category_name(self, category_minimal: Category, name: str) -> None:
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
    def test_invalid_category_name(
        self, category_minimal: Category, name: str, expected_error_message: str
    ) -> None:
        with pytest.raises(ValueError, match=expected_error_message):
            category_minimal.name = name

    def test_category_id_set_once_only(self, category_full) -> None:
        with pytest.raises(AttributeError, match='Идентификатор категории уже установлен'):
            category_full.id = 2
