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

    NOTSET = "notset"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


class LoggingSettings(BaseModel):
    level: LogLevel = LogLevel.DEBUG
    logger_name: str = f"{PACKAGE_NAME}_logger"


class FirestoreSettings(BaseSettings):
    prefix: str = ""
    database: str = ""


class SentrySettings(BaseSettings):
    dsn: str = ""
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0


class DiscordSettings(BaseSettings):
    guild_id: int = 1118283948016017449
    webhook_base_url: str = "https://discord.com/api/webhooks"
    notifications_channel_id: int = 1217594301324726292
    notifications_webhook_id: str = ""


class JWTSettings(BaseSettings):
    next_secret: str = ""
    next_cookie_name: str = "next-auth.session-token"
    next_cookie_prefix: str = "__Secure-"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    session_timeout_minutes: int = 60 * 24 * 365 * 2


class Server(BaseModel):
    port: int = 8080
    host: str = "0.0.0.0"
    reload: bool = False
    service: str | None = None
    tag: str | None = None
    workers: int = 1

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
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.dev", ".env.prod"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    firestore: FirestoreSettings = FirestoreSettings()
    sentry: SentrySettings = SentrySettings()
    jwt: JWTSettings = JWTSettings()
    discord: DiscordSettings = DiscordSettings()

    @property
    def next_cookie(self) -> str:
        if self.environment == Environment.PROD:
            return self.jwt.next_cookie_prefix + self.jwt.next_cookie_name
        return self.jwt.next_cookie_name

    @property
    def mm_session_cookie(self) -> str:
        return "MM_SESSION"

    @property
    def mm_profile_cookie(self) -> str:
        return "MM_PROFILE"

    @property
    def domain(self) -> str:
        if self.environment == Environment.PROD:
            return "modelmind.me"
        return "localhost"


settings = Settings()
