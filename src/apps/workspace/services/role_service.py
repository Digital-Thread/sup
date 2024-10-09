from typing import Any, Callable
from uuid import UUID

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.dtos.role_dtos import RoleAppDTO
from src.apps.workspace.repositories.i_role_repository import IRoleRepository
from src.apps.workspace.services.base_service import BaseService


class RoleService(BaseService[Role, RoleAppDTO, int, IRoleRepository]):
    pass
