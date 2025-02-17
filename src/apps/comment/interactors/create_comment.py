from src.apps.comment import AddCommentDto, CommentOutDto
from src.apps.comment.mapper import CommentMapper
from src.apps.comment.domain import CommentEntity
from src.apps.comment.interactors.base_interactor import Interactor
from src.apps.comment.repository import ICommentRepository


class AddCommentInteractor(Interactor[AddCommentDto, CommentOutDto]):

    def __init__(self, comment_repository: ICommentRepository):
        self._repository = comment_repository

    async def execute(self, request: AddCommentDto) -> CommentOutDto:
        comment_entity = CommentMapper.dto_to_entity(request)

        c: CommentEntity = await self._repository.save(comment_entity)
        response_dto: CommentOutDto = CommentMapper.entity_to_dto(c)
        return response_dto
