import typer
import uvicorn

from modelmind.config import PACKAGE_NAME, App, settings

cli = typer.Typer(name="{PACKAGE_NAME} Api")


@cli.command()
def run(
    app: App = App.MAIN,
    port: int = settings.server.port,
    host: str = settings.server.host,
    log_level: str = settings.logging.level.value,
    reload: bool = settings.server.reload,
    workers: int = settings.server.workers,
) -> None:
    uvicorn.run(
        f"{PACKAGE_NAME}.api.app:{app.value}",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        workers=workers,
    )


@cli.command(name="schedule-calculate-persony-statistics-tasks")
def schedule_calculate_persony_statistics_tasks() -> None:
    import asyncio

    from google.cloud.tasks_v2 import CloudTasksAsyncClient

    from modelmind.clients.firestore.client import initialize_firestore_client
    from modelmind.commands.schedule_persony_statistics import SchedulePersonyStatisticsCommand

    async def run_command() -> None:
        firestore_client = initialize_firestore_client()
        cloud_tasks_client = CloudTasksAsyncClient()
        command = SchedulePersonyStatisticsCommand(
            firestore_client=firestore_client, cloud_tasks_client=cloud_tasks_client
        )
        await command.run()

    asyncio.run(run_command())
