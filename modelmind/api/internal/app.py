from contextlib import asynccontextmanager
from typing import AsyncGenerator

import google.cloud.logging as logging
from fastapi import APIRouter, FastAPI
from fastapi.datastructures import State as FastAPIState
from fastapi.responses import UJSONResponse
from google.cloud import bigquery, firestore
from google.cloud.logging import Logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from modelmind.api.internal import health_router, statistics_router
from modelmind.config import PACKAGE_NAME, settings
from modelmind.logger import log
from modelmind.services.firestore.client import initialize_firestore_client
from modelmind.services.monitoring.cloud_trace import meter_provider, tracer_provider
from modelmind.services.monitoring.error_reporting import ErrorReporting

from .middleware import setup_middlewares


class InternalAPI(FastAPI):
    class State(FastAPIState):
        firestore: firestore.AsyncClient
        bigquery: bigquery.Client
        logging: logging.Client | None
        logger: Logger | None
        error_reporting: ErrorReporting | None

    state: State


def app() -> InternalAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    from modelmind.services.bigquery.client import BigqueryClient

    @asynccontextmanager
    async def lifespan(app: InternalAPI) -> AsyncGenerator[None, None]:
        # On startup
        log.info("Starting up")
        app.state.firestore = initialize_firestore_client()
        app.state.bigquery = BigqueryClient()
        app.state.logging = logging.Client()
        app.state.logger = app.state.logging.logger(PACKAGE_NAME)
        app.state.error_reporting = ErrorReporting(service=PACKAGE_NAME)
        app.build_middleware_stack()
        yield
        # On shutdown
        log.info("Shutting down")

    app = InternalAPI(
        title=PACKAGE_NAME + " Internal API",
        version="0.1.0",
        docs_url=f"{settings.server.prefix}/docs",
        redoc_url=f"{settings.server.prefix}/redoc",
        openapi_url=f"{settings.server.prefix}/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    FastAPIInstrumentor().instrument_app(
        app,
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
    )
    # Main router for the API.
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(router=statistics_router)
    v1_router.include_router(router=health_router)

    app.include_router(router=v1_router, prefix=settings.server.prefix)
    log.info("Public API v1 router included")

    # see middleware.py
    setup_middlewares(app)
    log.info("Middlewares set up")

    return app
