from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.dtos.category_dtos import CategoryAppDTO
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository
from src.apps.workspace.services.base_service import BaseService


class CategoryService(BaseService[Category, CategoryAppDTO, int, ICategoryRepository]):
    pass
