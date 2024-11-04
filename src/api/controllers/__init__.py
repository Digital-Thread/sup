from fastapi import FastAPI

from .feature import feature_router
from .health_check import router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(router=feature_router, prefix=f'{prefix}/features', tags=['Feature'])


__all__ = ('init_routes',)
