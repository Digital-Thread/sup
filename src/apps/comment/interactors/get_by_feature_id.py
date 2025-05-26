from src.apps.comment.domain import FeatureId
from src.apps.comment.dtos import CommentOutDto, FetchFeatureCommentDto
from src.apps.comment.interactors.base_interactor import BaseInteractor
from src.apps.comment.repository import ICommentRepository


class GetCommentsByFeatureIdInteractor(BaseInteractor):
    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: FetchFeatureCommentDto) -> list[CommentOutDto]:
        comments = await self._repository.get_by_feature_id(
            feature_id=FeatureId(request.feature_id),
            page=request.page,
            page_size=request.page_size,
        )
        return comments
