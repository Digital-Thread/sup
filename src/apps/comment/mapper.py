from src.apps.comment import CommentOutDto
from src.apps.comment.domain import AuthorId, FeatureId, TaskId
from src.apps.comment.domain.comment import CommentEntity
from src.apps.comment.dtos import BaseCommentDto


class CommentMapper:
    @staticmethod
    def entity_to_dto(entity: CommentEntity) -> CommentOutDto:
        return CommentOutDto(
            comment_id=entity.comment_id,
            task_id=entity.task_id if entity.task_id is not None else None,
            feature_id=entity.feature_id if entity.feature_id is not None else None,
            content=entity.content,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def dto_to_entity(dto: BaseCommentDto) -> CommentEntity:
        return CommentEntity.create_for_entity(
            user_id=AuthorId(dto.user_id),
            task_id=TaskId(dto.task_id) if dto.task_id is not None else None,
            feature_id=FeatureId(dto.feature_id) if dto.feature_id is not None else None,
            content=dto.content,
        )
