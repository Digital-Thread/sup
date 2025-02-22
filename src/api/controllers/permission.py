from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from apps.permission import GetPermissionsInteractor
from src.api.dtos import PermissionResponseDTO

permission_router = APIRouter(route_class=DishkaRoute)


@permission_router.get('/', status_code=status.HTTP_200_OK, response_model=list[PermissionResponseDTO])
async def get_permissions(
        interactor: FromDishka[GetPermissionsInteractor],
) -> list[PermissionResponseDTO]:
    permissions = await interactor.execute()
    return [PermissionResponseDTO(**asdict(perm)) for perm in permissions] if permissions else []
