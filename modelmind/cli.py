import typer
import uvicorn

from modelmind.config import PACKAGE_NAME, settings

cli = typer.Typer(name="{PACKAGE_NAME} Api")


@cli.command()
def run(
    port: int = settings.server.port,
    host: str = settings.server.host,
    log_level: str = settings.logging.level.value,
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
