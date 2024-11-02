from dishka import Provider, Scope, provide

from src.apps.comment import (
    AddCommentDto,
    AddCommentInteractor,
    CommentOutDto,
    CommentPaginationDto,
    DeleteCommentDto,
    DeleteCommentInteractor,
    FetchAllCommentsInteractor,
    FetchAllFeatureCommentsInteractor,
    FetchAllTaskCommentsInteractor,
    FetchCommentDto,
    FetchCommentInteractor,
    FetchFeatureCommentDto,
    FetchTaskCommentDto,
    UpdateCommentDto,
    UpdateCommentInteractor,
)
from src.apps.comment.domain import Interactor


class InteractorProvider(Provider):
    scope = Scope.REQUEST
    comment = provide(AddCommentInteractor, provides=Interactor[AddCommentDto, CommentOutDto])
    fetch_comment = provide(
        FetchCommentInteractor, provides=Interactor[FetchCommentDto, CommentOutDto]
    )
    fetch_comments = provide(
        FetchAllCommentsInteractor, provides=Interactor[CommentPaginationDto, list[CommentOutDto]]
    )
    update_comment = provide(
        UpdateCommentInteractor, provides=Interactor[UpdateCommentDto, CommentOutDto]
    )
    delete_comment = provide(DeleteCommentInteractor, provides=Interactor[DeleteCommentDto, None])
    fetch_task_comments = provide(
        FetchAllTaskCommentsInteractor,
        provides=Interactor[FetchTaskCommentDto, list[CommentOutDto]],
    )

    fetch_feature_comments = provide(
        FetchAllFeatureCommentsInteractor,
        provides=Interactor[FetchFeatureCommentDto, list[CommentOutDto]],
    )
