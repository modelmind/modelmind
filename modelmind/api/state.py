from typing import Any

import google.cloud.bigquery as bigquery
import google.cloud.firestore as firestore
import google.cloud.logging as logging
import google.cloud.storage as storage
import httpx
from fastapi import Request
from fastapi.datastructures import State as FastAPIState
from google.cloud.logging import Logger

from modelmind.services.monitoring.error_reporting import ErrorReporting


class AppState(FastAPIState):
    firestore: firestore.AsyncClient | None
    storage: storage.Client | None
    logging: logging.Client | None
    logger: Logger | None
    error_reporting: ErrorReporting | None
    httpx_client: httpx.AsyncClient | None
    bigquery: bigquery.Client | None

    def __getattr__(self, name: str) -> Any:
        annotations = self.__annotations__
        if name in annotations:
            value = super().__getattr__(name)
            if value is None:
                raise ValueError(f"'{name}' has not been initialized for this App.")
            return value
        else:
            return super().__getattr__(name)


async def get_app_state(request: Request) -> AppState:
    return request.app.state
