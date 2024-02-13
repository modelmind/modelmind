import enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, enum.Enum):
    DEV = "dev"
    PROD = "prod"


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class FirebaseSettings(BaseSettings):
    prefix: str = ""


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = 8080
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.DEBUG

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.dev", ".env.prod"),
        env_prefix="MODELMIND_",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    firebase: FirebaseSettings = FirebaseSettings()


settings = Settings()
