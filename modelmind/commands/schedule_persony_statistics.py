from google.cloud import firestore
from google.cloud.tasks_v2 import CloudTasksAsyncClient

from modelmind.config import settings
from modelmind.db.schemas.settings import SchedulerSettings
from modelmind.logger import log
from modelmind.services.create_cloud_task import create_task

from .base import Command


class SchedulePersonyStatisticsCommand(Command[None]):
    def __init__(
        self,
        cloud_tasks_client: CloudTasksAsyncClient,
        firestore_client: firestore.AsyncClient,
    ) -> None:
        self.cloud_tasks_client = cloud_tasks_client
        self.firestore_client = firestore_client

    async def get_scheduler_settings(self) -> SchedulerSettings:
        scheduler_settings_ref = self.firestore_client.collection("settings").document("scheduler")
        return (await scheduler_settings_ref.get()).to_dict()

    async def _run(self) -> None:
        scheduler_settings = await self.get_scheduler_settings()

        statistics_scheduler_settings = scheduler_settings["statistics"]

        questionnaire_ids = statistics_scheduler_settings["persony"]

        for questionnaire_id in questionnaire_ids:
            task = await create_task(
                client=self.cloud_tasks_client,
                project=settings.tasks_queue_calculate_statistics.project,
                location=settings.tasks_queue_calculate_statistics.location,
                queue=settings.tasks_queue_calculate_statistics.queue,
                url=f"{settings.server.base_url}/v1/internal/statistics/persony",
                deadline_in_seconds=1200,
                json_payload={
                    "questionnaire_id": questionnaire_id,
                },
            )
            log.info(task)
