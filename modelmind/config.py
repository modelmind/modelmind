from enum import Enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())
PACKAGE_NAME = Path(__file__).parent.name
ENV_PREFIX = f"{PACKAGE_NAME.upper()}_"


class Server(BaseModel):
    port: int = 8080
    host: str = "0.0.0.0"
    log_level: str = "debug"
    reload: bool = False
    service: str | None = None
    tag: str | None = None
    workers: int = 4
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


class ElasticSettings(BaseModel):
    service_name: str | None = None
    server_url: str | None = None
    api_key: str | None = None


class Environment(str, Enum):
    PREPROD = "preprod"
    PROD = "prod"
    LOCAL = "local"


class LoggingSettings(BaseModel):
    log_level: str = "INFO"
    logger_name: str = f"{PACKAGE_NAME}_logger"


class Gainsight(BaseSettings):
    api_key: str = ""
    base_url: str = "https://agicap.eu.gainsightcloud.com"


class AgicapGateway(BaseSettings):
    # base_url: str = "http://0.0.0.0:8080"
    base_url: str = "https://agicap-gateway.agicap-lab.com/prod"


class Settings(BaseSettings):
    server: Server = Server()
    elastic: ElasticSettings = ElasticSettings()
    environment: Environment = Environment.LOCAL
    logger: LoggingSettings = LoggingSettings()
    agicap_gateway: AgicapGateway = AgicapGateway()
    gainsight: Gainsight = Gainsight()

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.dev", ".env.prod"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
