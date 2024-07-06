from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.statistics import PersonyStatistics
from modelmind.services.event_notifier import EventNotifier

from .base import Command


class SendPersonyStatisticsNotificationCommand(Command[None]):
    def __init__(
        self,
        questionnaire: DBQuestionnaire,
        statistics: PersonyStatistics,
        event_notifier: EventNotifier,
    ) -> None:
        self.questionnaire = questionnaire
        self.statistics = statistics
        self.event_notifier = event_notifier

    async def _run(self) -> None:
        await self.event_notifier.new_statistics(self.questionnaire, self.statistics)
