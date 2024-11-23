import abc
import traceback
import typing
from contextlib import contextmanager
from datetime import datetime
from enum import StrEnum

from fastapi.requests import Request
from google.cloud.logging import Logger
from opentelemetry.trace import Span
from opentelemetry.util.types import Attributes

from modelmind.config import Environment, settings


class SeverityLevel(StrEnum):
    DEFAULT = "DEFAULT"
    DEBUG = "DEBUG"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    ALERT = "ALERT"
    EMERGENCY = "EMERGENCY"


def _parse_content_length(content_header: str | None) -> int | None:
    if content_header is None:
        return None
    try:
        content_length = int(content_header)
    except (ValueError, TypeError):
        content_length = None
    return content_length


class BaseContext(abc.ABC):
    @abc.abstractproperty
    def trace_id(self) -> str:
        raise NotImplementedError()

    def mark_span_as_error(self) -> None:
        raise NotImplementedError()

    @abc.abstractproperty
    def span_id(self) -> str:
        raise NotImplementedError()

    @contextmanager
    def build_sub_context(self, name: str) -> typing.Generator[typing.Self, None, None]:
        yield self

    @abc.abstractmethod
    def set_status_code(self, status: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def set_latency(self, latency: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def send_event(self, name: str, event: Attributes) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def exception(self, exception: Exception) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def log(self, message: str, severity: SeverityLevel, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def default(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def debug(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def info(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def notice(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def warning(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def error(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def critical(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def alert(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def emergency(self, message: str, **kwargs: object) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def list_logs_by_trace_id(
        self,
        trace_id: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def list_logs_by_trace_and_span_id(
        self,
        trace_id: str,
        span_id: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[str]:
        raise NotImplementedError()


class Context(BaseContext):
    MAX_LOG_SIZE = 256 * 1024  # 256 KB

    def __init__(self, request: Request, span: Span, logger: Logger) -> None:
        remote_ip_default_value = request.client.host if request.client else None
        self._http_request = {
            "requestMethod": request.method,
            "requestUrl": str(request.url),
            "userAgent": request.headers.get("user-agent"),
            "remoteIp": request.headers.get("x-forwarded-for", remote_ip_default_value),  # type: ignore
            "referer": request.headers.get("referer"),
            "protocol": request.headers.get("request.url.scheme"),
            "requestSize": _parse_content_length(request.headers.get("content-length")),
        }

        self._trace_id = span.get_span_context().trace_id.to_bytes(16, "big").hex()
        self._span_id = span.get_span_context().span_id.to_bytes(8, "big").hex()
        self._logger = logger
        self._span = span
        self._cloud_trace_id = f"projects/aidenlearn1/traces/{self.trace_id}"

    @property
    def trace_id(self) -> str:
        return self._trace_id

    @property
    def span_id(self) -> str:
        return self._span_id

    def set_status_code(self, status: int) -> None:
        self._http_request["status"] = status

    def set_latency(self, latency: str) -> None:
        self._http_request["latency"] = latency

    def send_event(self, name: str, event: Attributes) -> None:
        self._span.add_event(name=name, attributes=event)

    def exception(self, exception: Exception) -> None:
        exception_msg = "".join(traceback.format_exception(exception))
        self.log(message=exception_msg, severity=SeverityLevel.ERROR)
        self._span.record_exception(exception)

    def log(self, message: str, severity: SeverityLevel, **kwargs: object) -> None:
        self._logger.log_struct(
            {"message": self._truncate_message(message), **kwargs},
            http_request=self._http_request,
            severity=severity,
            trace=self._cloud_trace_id,
            span_id=self.span_id,
        )
        if settings.environment == Environment.LOCAL:
            print(f"{severity}: {message}")
        else:
            print("event logged", settings.environment)

    def default(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.DEFAULT, **kwargs)

    def debug(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.DEBUG, **kwargs)

    def info(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.INFO, **kwargs)

    def notice(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.NOTICE, **kwargs)

    def warning(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.WARNING, **kwargs)

    def error(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.ERROR, **kwargs)

    def critical(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.CRITICAL, **kwargs)

    def alert(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.ALERT, **kwargs)

    def emergency(self, message: str, **kwargs: object) -> None:
        self.log(message=message, severity=SeverityLevel.EMERGENCY, **kwargs)

    def list_logs_by_trace_id(
        self,
        trace_id: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[str]:
        filter = [
            f'trace="projects/{self._logger.project}/traces/{trace_id}"',
        ]
        if start_datetime:
            filter.append(f'timestamp >= "{start_datetime.isoformat()}"')
        if end_datetime:
            filter.append(f'timestamp >= "{end_datetime.isoformat()}"')
        entries = self._logger.list_entries(filter_=" ".join(filter))
        return [entry.payload.get("message", "") for entry in entries]

    def list_logs_by_trace_and_span_id(
        self,
        trace_id: str,
        span_id: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[str]:
        filter = [
            f'trace="projects/{self._logger.project}/traces/{trace_id}"',
            f'spanId="{span_id}"',
        ]
        if start_datetime:
            filter.append(f'timestamp >= "{start_datetime.isoformat()}"')
        if end_datetime:
            filter.append(f'timestamp >= "{end_datetime.isoformat()}"')
        entries = self._logger.list_entries(filter_=" ".join(filter))
        return [entry.payload.get("message", "") for entry in entries]

    def _truncate_message(self, message: str) -> str:
        encoded_message = message.encode("utf-8")
        if len(encoded_message) > self.MAX_LOG_SIZE - 1024:
            truncated_message = encoded_message[: self.MAX_LOG_SIZE - 1024].decode("utf-8", errors="ignore")
            return truncated_message + "..."
        return message
