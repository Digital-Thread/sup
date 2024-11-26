from uuid import UUID
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status, Path, Query

from src.api.dtos.category import (
    CreateCategoryDTO,
    CategoryResponseDTO,
    UpdateCategoryDTO,
)
from src.apps.workspace.dtos.category_dtos import (
    CreateCategoryAppDTO,
    DeleteCategoryAppDTO,
    GetCategoriesAppDTO,
    UpdateCategoryAppDTO,
)
from src.apps.workspace.exceptions.category_exceptions import CategoryException
from src.apps.workspace.interactors.category_interactors import (
    CreateCategoryInteractor,
    DeleteCategoryInteractor,
    GetCategoryByWorkspaceInteractor,
    UpdateCategoryInteractor,
)
from src.apps.workspace.interactors.category_interactors.get_category_by_id import GetCategoryByIdInteractor

category_router = APIRouter(route_class=DishkaRoute)


@category_router.post('', status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CreateCategoryDTO, interactor: FromDishka[CreateCategoryInteractor]
) -> dict[str, str]:
    request = CreateCategoryAppDTO(**body.model_dump())
    try:
        await interactor.execute(request)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect': '/'}


@category_router.get('/', status_code=status.HTTP_200_OK, response_model=list[CategoryResponseDTO])
async def get_categories_by_workspace_id(
    workspace_id: UUID, interactor: FromDishka[GetCategoryByWorkspaceInteractor]
) -> list[CategoryResponseDTO]:
    try:
        response = await interactor.execute(GetCategoriesAppDTO(workspace_id=workspace_id))
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return [CategoryResponseDTO(**category.__dict__) for category in response]


@category_router.get('/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseDTO)
async def get_category_by_id(
        category_id: Annotated[int, Path()],
        workspace_id: Annotated[UUID, Query()],
        interactor: FromDishka[GetCategoryByIdInteractor]
) -> CategoryResponseDTO:
    try:
        response = await interactor.execute(category_id, workspace_id)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return CategoryResponseDTO(**response.__dict__)


@category_router.patch('/{category_id}', status_code=status.HTTP_200_OK)
async def update_category(
    body: UpdateCategoryDTO,
    workspace_id: UUID,
    category_id: int,
    interactor: FromDishka[UpdateCategoryInteractor],
) -> dict[str, str]:
    request = UpdateCategoryAppDTO(
        **body.model_dump(exclude_none=True), id=category_id, workspace_id=workspace_id
    )
    try:
        await interactor.execute(request)
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {'redirect_url': '/'}


@category_router.delete('/{category_id}')
async def delete_category_by_id(
    category_id: int, workspace_id: UUID, interactor: FromDishka[DeleteCategoryInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(DeleteCategoryAppDTO(id=category_id, workspace_id=workspace_id))
    except CategoryException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {'redirect_url': '/'}
