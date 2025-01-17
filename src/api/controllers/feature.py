from dataclasses import asdict
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.api.dtos.feature import (
    CreateFeatureRequestDTO,
    FeatureResponseDTO,
    QueryParams,
    SuccessResponse,
    UpdateFeatureRequestDTO,
)
from src.apps.feature.interactors import (
    CreateFeatureInteractor,
    DeleteFeatureInteractor,
    GetAllFeaturesInteractor,
    GetFeatureInteractor,
    UpdateFeatureInteractor,
)
from src.apps.feature.domain import FeatureId, OptionalFeatureUpdateFields, WorkspaceId
from src.apps.feature import FeatureListQuery, FeatureInputDTO, FeatureUpdateDTO, OrderBy, PaginateParams
from src.providers.context import WorkspaceContext

feature_router = APIRouter(route_class=DishkaRoute)


@feature_router.post('/', status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_feature(
        dto: CreateFeatureRequestDTO,
        interactor: FromDishka[CreateFeatureInteractor],
        context: FromDishka[WorkspaceContext],
) -> SuccessResponse:
    workspace_id = context.workspace_id
    feature = FeatureInputDTO(WorkspaceId(workspace_id), **dto.model_dump())
    await interactor.execute(dto=feature)

    return SuccessResponse(message='Feature created')


@feature_router.get('/', status_code=status.HTTP_200_OK, response_model=list[FeatureResponseDTO])
async def get_features(
        query: Annotated[QueryParams, Query()],
        interactor: FromDishka[GetAllFeaturesInteractor],
        context: FromDishka[WorkspaceContext],
) -> list[FeatureResponseDTO]:
    workspace_id = WorkspaceId(context.workspace_id)
    query_params = FeatureListQuery(
        filters=query.filters,
        order_by=OrderBy(field=query.order_by_field, order=query.sort_order),
        paginate_by=PaginateParams(offset=query.offset, limit_by=query.per_page.limit_by),
    )
    features = await interactor.execute(workspace_id=workspace_id, query=query_params)
    return [FeatureResponseDTO(**asdict(feature)) for feature in features] if features else []


@feature_router.get(
    '/{feature_id}', status_code=status.HTTP_200_OK, response_model=FeatureResponseDTO
)
async def get_feature_by_id(
        feature_id: FeatureId,
        interactor: FromDishka[GetFeatureInteractor],
) -> FeatureResponseDTO:
    feature = await interactor.execute(feature_id=feature_id)
    return FeatureResponseDTO(**asdict(feature))


@feature_router.patch(
    '/{feature_id}', status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
async def update_feature(
        feature_id: FeatureId,
        dto: UpdateFeatureRequestDTO,
        interactor: FromDishka[UpdateFeatureInteractor],
) -> SuccessResponse:
    update_data = FeatureUpdateDTO(
        id=feature_id,
        updated_fields=OptionalFeatureUpdateFields(**dto.model_dump(exclude_unset=True)),
    )
    await interactor.execute(update_data)
    return SuccessResponse(message='Feature updated')


@feature_router.delete('/{feature_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature(
        feature_id: FeatureId,
        interactor: FromDishka[DeleteFeatureInteractor],
) -> None:
    await interactor.execute(feature_id=feature_id)
