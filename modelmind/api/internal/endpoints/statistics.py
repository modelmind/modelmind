from fastapi import APIRouter, Body, Depends

from modelmind.api.internal.dependencies.clients.bigquery import get_bigquery_client
from modelmind.api.internal.dependencies.notifier import get_event_notifier
from modelmind.api.internal.schemas.requests import CalculateStatisticsRequest
from modelmind.api.public.dependencies.daos.providers import questionnaires_dao_provider
from modelmind.commands.calculate_persony_statistics import CalculatePersonyStatisticsCommand
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.services.bigquery.client import BigqueryClient
from modelmind.services.event_notifier import EventNotifier

router = APIRouter(prefix="/statistics")


@router.post("/persony")
async def calculate_questionnaire_statistics(
    request: CalculateStatisticsRequest = Body(...),
    bigquery_client: BigqueryClient = Depends(get_bigquery_client),
    questionnaires_dao: QuestionnairesDAO = Depends(questionnaires_dao_provider),
    event_notifier: EventNotifier = Depends(get_event_notifier),
) -> None:
    await CalculatePersonyStatisticsCommand(
        questionnaire_id=request.questionnaire_id,
        bigquery_client=bigquery_client,
        questionnaires_dao=questionnaires_dao,
        event_notifier=event_notifier,
    ).run()
