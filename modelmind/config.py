from enum import Enum, auto
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

    NOTSET = "notset"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


class FirebaseSettings(BaseSettings):
    prefix: str = ""


class SentrySettings(BaseSettings):
    dsn: str = ""
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0


class JWTSettings(BaseSettings):
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7


class Server(BaseModel):
    port: int = 8080
    host: str = "0.0.0.0"
    log_level: str = LogLevel.DEBUG.value
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
    jwt: JWTSettings = JWTSettings()


settings = Settings()
