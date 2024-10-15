from src.apps.comment import AddCommentToTaskDto, CommentOutDto
from src.apps.comment.converters import CommentMapper
from src.apps.comment.domain import (
    CommentEntity,
    CommentId,
    ICommentRepository,
    Interactor,
)


class AddCommentToTaskInteractor(Interactor[AddCommentToTaskDto, CommentOutDto]):

    def __init__(self, comment_repository: ICommentRepository[CommentId, CommentEntity]):
        self._repository = comment_repository

    def execute(self, request: AddCommentToTaskDto) -> CommentOutDto:
        comment_entity = CommentMapper.dto_to_entity(request)

        c: CommentEntity = self._repository.save(comment_entity)
        response_dto: CommentOutDto = CommentMapper.entity_to_dto(c)
        return response_dto
