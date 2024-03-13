from abc import ABC
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

import httpx
from httpx._models import Response
from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    URLTypes,
)


class HttpxClient(ABC):
    def __init__(self, base_url: str, timeout: int = 8000, bearer_token: Optional[str] = None) -> None:
        self.bearer_token = bearer_token
        self.base_url = base_url
        self.timeout = timeout
        self._headers = self._default_headers

    @staticmethod
    def _raise_on_4xx_5xx(response: httpx.Response) -> None:
        response.raise_for_status()

    @property
    def _default_headers(self) -> dict:
        default_headers = {"content-type": "application/json"}
        if self.bearer_token:
            default_headers["Authorization"] = f"Bearer {self.bearer_token}"
        return default_headers

    def set_header(self, key: str, value: str) -> None:
        self._headers[key] = value

    @asynccontextmanager
    async def _aclient(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            event_hooks={"response": [self._raise_on_4xx_5xx]},
            headers=self._headers,
            timeout=self.timeout,
        ) as client:
            yield client

    async def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: Optional[RequestContent] = None,
        data: Optional[RequestData] = None,
        files: Optional[RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
        cookies: Optional[CookieTypes] = None,
        extensions: Optional[RequestExtensions] = None,
    ) -> Response:
        async with self._aclient() as client:
            return await client.request(
                method,
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                extensions=extensions,
            )
