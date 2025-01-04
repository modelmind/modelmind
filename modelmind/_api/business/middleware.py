from time import time
from typing import cast

from fastapi import FastAPI, Request, Response
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from modelmind.config import PACKAGE_NAME, Environment, settings
from modelmind.services.monitoring.cloud_trace import trace
from modelmind.services.monitoring.trace_context import BaseContext, Context


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors.allow_origins,
        allow_credentials=settings.server.cors.allow_credentials,
        allow_methods=settings.server.cors.allow_methods,
        allow_headers=settings.server.cors.allow_headers,
        expose_headers=settings.server.cors.expose_headers,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
        ctx = cast(BaseContext, request.scope.get("context"))
        # error_context = HTTPContext(
        #     method=request.method,
        #     url=request.url.path,
        #     user_agent=request.headers.get("user-agent"),
        #     referrer=request.headers.get("referer"),
        #     response_status_code=422,
        #     remote_ip=request.client.host if request.client else None,
        # )
        if ctx:
            ctx.error(f"{PACKAGE_NAME}: Request Validation Error, bad arguments {request.url.path}")
            ctx.exception(exc)
        # request.app.state.error_reporting.report_exception(context=error_context)
        return await request_validation_exception_handler(request, exc)

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> Response:
        ctx = cast(BaseContext, request.scope.get("context"))
        # error_context = HTTPContext(
        #     method=request.method,
        #     url=request.url.path,
        #     user_agent=request.headers.get("user-agent"),
        #     referrer=request.headers.get("referer"),
        #     response_status_code=exc.status_code,
        #     remote_ip=request.client.host if request.client else None,
        # )
        if ctx:
            ctx.error(f"{PACKAGE_NAME}: {request.url.path} {exc.status_code}")
            ctx.exception(exc)
        # request.app.state.error_reporting.report_exception(context=error_context)
        return await http_exception_handler(request, exc)


def setup_middlewares(app: FastAPI) -> None:
    setup_cors(app)
    setup_exception_handlers(app)

    @app.middleware("http")
    async def provide_context(request: Request, call_next) -> Response:
        begin = time()
        ctx = Context(
            request=request,
            span=trace.get_current_span(),
            logger=request.app.state.logger,
        )
        request.scope["context"] = ctx
        response = await call_next(request)
        latency = time() - begin
        ctx.set_latency(f"{latency}s")
        ctx.set_status_code(response.status_code)

        response.headers["X-Transaction-Id"] = ctx.trace_id

        if settings.environment != Environment.PROD:
            response.headers["X-latency"] = f"{latency}s"

        return response
