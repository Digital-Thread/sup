from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.category_dtos import (
    CreateCategoryDTO,
    ResponseCategoryDTO,
    UpdateCategoryDTO,
)
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import (
    CreateCategoryAppDTO,
    UpdateCategoryAppDTO,
)
from src.apps.workspace.exceptions.category_exceptions import CategoryException
from src.apps.workspace.use_cases.category_use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryByWorkspaceUseCase,
    UpdateCategoryUseCase,
)

category_router = APIRouter(route_class=DishkaRoute)


@category_router.post('/create_category', status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CreateCategoryDTO, use_case: FromDishka[CreateCategoryUseCase]
) -> dict[str, str]:
    request = CreateCategoryAppDTO(**body.model_dump())
    try:
        await use_case.execute(request)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect': '/'}


@category_router.get('/', status_code=status.HTTP_200_OK, response_model=list[ResponseCategoryDTO])
async def get_categories_by_workspace_id(
    workspace_id: WorkspaceId, use_case: FromDishka[GetCategoryByWorkspaceUseCase]
) -> list[ResponseCategoryDTO]:
    try:
        response = await use_case.execute(workspace_id)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return [ResponseCategoryDTO(**category.__dict__) for category in response]


@category_router.patch('/{category_id}', status_code=status.HTTP_200_OK)
async def update_category(
    body: UpdateCategoryDTO,
    workspace_id: WorkspaceId,
    category_id: CategoryId,
    use_case: FromDishka[UpdateCategoryUseCase],
) -> dict[str, str]:
    request = UpdateCategoryAppDTO(**body.model_dump(exclude_none=True))
    try:
        await use_case.execute(category_id, workspace_id, request)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@category_router.delete('/{category_id}')
async def delete_category_by_id(
    category_id: CategoryId, workspace_id: WorkspaceId, use_case: FromDishka[DeleteCategoryUseCase]
) -> dict[str, str]:
    try:
        await use_case.execute(category_id, workspace_id)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
