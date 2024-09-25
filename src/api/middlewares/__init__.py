from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from .logging import logging_middleware


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=logging_middleware,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=False,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['Content-Disposition'],
    )


__all__ = ('init_middlewares',)
