from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from modelmind.api import monitoring_router, public_v1_router
from modelmind.config import PACKAGE_NAME, settings

from .middleware import setup_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # On startup
    print("Starting up")
    app.build_middleware_stack()
    yield
    # On shutdown
    print("Shutting down")


def main() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title=PACKAGE_NAME,
        version="0.1.0",
        docs_url=f"{settings.server.prefix}/docs",
        redoc_url=f"{settings.server.prefix}/redoc",
        openapi_url=f"{settings.server.prefix}/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    # Main router for the API.
    app.include_router(router=public_v1_router, prefix=settings.server.prefix)
    app.include_router(router=monitoring_router, prefix=settings.server.prefix)

    # see middleware.py
    setup_middlewares(app)

    return app
