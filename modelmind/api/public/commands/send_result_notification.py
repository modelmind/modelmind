from modelmind.db.daos.profiles import ProfilesDAO
from modelmind.db.schemas import DBIdentifier
from modelmind.models.questionnaires.base import Questionnaire
from modelmind.models.results.base import Result
from modelmind.services.event_notifier import EventNotifier

from .base import Command


class SendResultNotificationCommand(Command[None]):
    def __init__(
        self,
        questionnaire: Questionnaire,
        results: Result,
        event_notifier: EventNotifier,
        profile_id: DBIdentifier,
        profiles_dao: ProfilesDAO,
    ) -> None:
        self.questionnaire = questionnaire
        self.results = results
        self.event_notifier = event_notifier
        self.profile_id = profile_id
        self.profiles_dao = profiles_dao

    async def _run(self) -> None:
        analytics = self.questionnaire.get_analytics(self.results)
        db_profile = await self.profiles_dao.get_from_id(self.profile_id)

        await self.event_notifier.new_result(self.questionnaire.name, analytics, db_profile.biographics)
