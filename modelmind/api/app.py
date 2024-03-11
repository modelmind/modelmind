import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from modelmind.api import monitoring_router, public_v1_router
from modelmind.config import PACKAGE_NAME, Environment, settings

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

    logging.basicConfig(level=settings.server.log_level)

    sentry_sdk.init(
        dsn=settings.sentry.dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=settings.sentry.traces_sample_rate,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=settings.sentry.profiles_sample_rate,
        environment=settings.environment.value,
        debug=settings.environment == Environment.DEV,
        attach_stacktrace=True,
        enable_tracing=True,
    )

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
