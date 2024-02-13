import sentry_sdk
import typer
import uvicorn

from modelmind.config import PACKAGE_NAME, settings

sentry_sdk.init(
    dsn="https://2865092febf08a2155df759e146c0177@o4505461953265664.ingest.sentry.io/4506741397782528",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

cli = typer.Typer(name="Lab {PACKAGE_NAME} Api")


@cli.command()
def run(
    port: int = settings.server.port,
    host: str = settings.server.host,
    log_level: str = settings.server.log_level,
    reload: bool = settings.server.reload,
    workers: int = settings.server.workers,
) -> None:
    uvicorn.run(
        f"{PACKAGE_NAME}.api.app:main",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        workers=workers,
    )


@cli.command()
def hello_world() -> None:
    print("Hello World!")
