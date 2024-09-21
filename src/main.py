import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
import uvicorn
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api import init_exception_handlers, init_routes
from src.api.middlewares import init_middlewares
from src.providers.adapters import (
    ConfigProvider,
    RepositoriesProvider,
    SqlalchemyProvider,
)
from src.utils import log

logger = structlog.stdlib.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    if hasattr(app.state, 'container'):
        await app.state.container.close()


def container_factory() -> AsyncContainer:
    return make_async_container(
        SqlalchemyProvider(),
        ConfigProvider(),
        RepositoriesProvider(),
    )


def init_di(app: FastAPI) -> None:
    container = container_factory()
    setup_dishka(container, app)


def init_services(app: FastAPI) -> None:
    init_middlewares(app)
    log.configure_logging()


async def start_server(app: FastAPI) -> None:
    app_config = uvicorn.Config(
        app=app,
        host='0.0.0.0',
        port=8080,
        reload=True,
        use_colors=True,
        log_level='debug',
    )
    server = uvicorn.Server(config=app_config)
    await logger.info('Starting server')
    await server.serve()


def create_app() -> FastAPI:
    app = FastAPI(
        title='Sup API',
        version='0.1.0',
        swagger_ui_parameters={'syntaxHighlight.theme': 'obsidian'},
        lifespan=lifespan,
    )
    init_services(app)
    init_di(app)
    init_routes(app)
    init_exception_handlers(app)

    return app


if __name__ == '__main__':
    application = create_app()
    try:
        with asyncio.Runner() as runner:
            runner.run(start_server(application))
    except (KeyboardInterrupt, SystemExit):
        logging.info('Shutting down')
