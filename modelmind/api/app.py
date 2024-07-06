import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from fastapi.datastructures import State
from fastapi.responses import UJSONResponse
from google.cloud import bigquery, firestore
from sentry_sdk.integrations.logging import LoggingIntegration

from modelmind.api import internal_v1_router, public_v1_router
from modelmind.config import PACKAGE_NAME, Environment, settings
from modelmind.logger import log
from modelmind.services.firestore.client import initialize_firestore_client

from .middleware import setup_middlewares


class ModelMindPublicState(State):
    firestore: firestore.AsyncClient


class ModelMindPublicAPI(FastAPI):
    state: ModelMindPublicState


def main() -> ModelMindPublicAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    @asynccontextmanager
    async def lifespan(app: ModelMindPublicAPI) -> AsyncGenerator[None, None]:
        # On startup
        log.info("Starting up")
        app.state.firestore = initialize_firestore_client()
        app.build_middleware_stack()
        yield
        # On shutdown
        log.info("Shutting down")

    log.info("Initializing Sentry SDK...")
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
        integrations=[LoggingIntegration(level=logging.DEBUG, event_level=logging.ERROR)],
        default_integrations=True,
    )
    log.info("Sentry SDK initialized")

    app = ModelMindPublicAPI(
        title=PACKAGE_NAME,
        version="0.1.0",
        docs_url=f"{settings.server.prefix}/docs",
        redoc_url=f"{settings.server.prefix}/redoc",
        openapi_url=f"{settings.server.prefix}/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )
    log.info("FastAPI application created")

    # Main router for the API.
    app.include_router(router=public_v1_router, prefix=settings.server.prefix)
    log.info("Public API v1 router included")

    # see middleware.py
    setup_middlewares(app)
    log.info("Middlewares set up")

    return app


class ModelMindInternalState(State):
    firestore: firestore.AsyncClient
    bigquery: bigquery.Client


class ModelMindInternalAPI(FastAPI):
    state: ModelMindInternalState


def internal() -> ModelMindInternalAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    from modelmind.services.bigquery.client import BigqueryClient

    @asynccontextmanager
    async def lifespan(app: ModelMindInternalAPI) -> AsyncGenerator[None, None]:
        # On startup
        log.info("Starting up")
        app.state.firestore = initialize_firestore_client()
        app.state.bigquery = BigqueryClient()
        app.build_middleware_stack()
        yield
        # On shutdown
        log.info("Shutting down")

    app = ModelMindInternalAPI(
        title=PACKAGE_NAME + " Internal API",
        version="0.1.0",
        docs_url=f"{settings.server.prefix}/docs",
        redoc_url=f"{settings.server.prefix}/redoc",
        openapi_url=f"{settings.server.prefix}/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    # Main router for the API.
    app.include_router(router=internal_v1_router, prefix=settings.server.prefix)
    log.info("Public API v1 router included")

    # see middleware.py
    setup_middlewares(app)
    log.info("Middlewares set up")

    return app
