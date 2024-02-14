from enum import Enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())
PACKAGE_NAME = Path(__file__).parent.name
ENV_PREFIX = f"{PACKAGE_NAME.upper()}_"


class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"


class LogLevel(str, Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class FirebaseSettings(BaseSettings):
    prefix: str = ""


class SentrySettings(BaseSettings):
    dsn: str = ""
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0


class Server(BaseModel):
    port: int = 8080
    host: str = "0.0.0.0"
    log_level: LogLevel = LogLevel.DEBUG
    reload: bool = False
    service: str | None = None
    tag: str | None = None
    workers: int = 1
    include_my_account_router: bool = False
    include_runner_router: bool = False

    @property
    def prefix(self) -> str:
        prefixes = []
        if settings.server.service is not None:
            prefixes.append(settings.server.service)
        if settings.server.tag is not None:
            prefixes.append(settings.server.tag)

        if len(prefixes) > 0:
            return "/" + "/".join(prefixes)
        else:
            return ""


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """
    server: Server = Server()
    environment: Environment = Environment.DEV

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.dev", ".env.prod"),
        env_prefix="MODELMIND_",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    firebase: FirebaseSettings = FirebaseSettings()
    sentry: SentrySettings = SentrySettings()


settings = Settings()
