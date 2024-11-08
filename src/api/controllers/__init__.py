from fastapi import FastAPI

from .category import category_router
from .comment import comment_router
from .feature import feature_router
from .health_check import router
from .project import project_router
from .role import role_router
from .tag import tag_router
from .user import router as user_router
from .workspace import workspace_router
from .workspace_invite import workspace_invite_router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(
        router=user_router,
        prefix=f'{prefix}/user',
        tags=['Users'],
    )
    app.include_router(router=workspace_router, prefix=f'{prefix}/workspaces', tags=['Workspace'])
    app.include_router(router=role_router, prefix=f'{prefix}/roles', tags=['Role'])
    app.include_router(router=tag_router, prefix=f'{prefix}/tags', tags=['Tag'])
    app.include_router(router=category_router, prefix=f'{prefix}/categories', tags=['Category'])
    app.include_router(
        router=workspace_invite_router,
        prefix=f'{prefix}/workspace_invites',
        tags=['WorkspaceInvite'],
    )
    app.include_router(router=comment_router, prefix=f'{prefix}/comments', tags=['Comment'])
    app.include_router(router=project_router, prefix=f'{prefix}/projects', tags=['Project'])
    app.include_router(router=feature_router, prefix=f'{prefix}/features', tags=['Feature'])


__all__ = ('init_routes',)
