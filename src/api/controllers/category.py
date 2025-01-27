from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, status

from src.api.dtos.category import CategoryResponseDTO
from src.apps.workspace.interactors.category_interactors import (
    CreateCategoryInteractor,
    DeleteCategoryInteractor,
    GetCategoryByWorkspaceInteractor,
    UpdateCategoryInteractor,
)
from src.apps.workspace.interactors.category_interactors.get_category_by_id import (
    GetCategoryByIdInteractor,
)
from src.providers.context import WorkspaceContext

category_router = APIRouter(route_class=DishkaRoute)


@category_router.post('', status_code=status.HTTP_201_CREATED)
async def create_category(
    category_name: Annotated[str, Body()],
    interactor: FromDishka[CreateCategoryInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(category_name, context.workspace_id)


@category_router.get('/', status_code=status.HTTP_200_OK, response_model=list[CategoryResponseDTO])
async def get_categories_in_workspace(
    interactor: FromDishka[GetCategoryByWorkspaceInteractor], context: FromDishka[WorkspaceContext]
) -> list[CategoryResponseDTO]:
    response = await interactor.execute(workspace_id=context.workspace_id)
    return [CategoryResponseDTO(**category.__dict__) for category in response]


@category_router.get(
    '/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseDTO
)
async def get_category_by_id(
    category_id: Annotated[int, Path()],
    interactor: FromDishka[GetCategoryByIdInteractor],
    context: FromDishka[WorkspaceContext],
) -> CategoryResponseDTO:
    response = await interactor.execute(category_id=category_id, workspace_id=context.workspace_id)
    return CategoryResponseDTO(**response.__dict__)


@category_router.patch('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_category(
    category_name: Annotated[str, Body()],
    category_id: Annotated[int, Path()],
    interactor: FromDishka[UpdateCategoryInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(
        category_id=category_id, category_name=category_name, workspace_id=context.workspace_id
    )


@category_router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(
    category_id: int,
    interactor: FromDishka[DeleteCategoryInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(category_id=category_id, workspace_id=context.workspace_id)
