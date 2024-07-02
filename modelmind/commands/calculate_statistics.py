from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator

from bigquery.queries.calculate_accuracy import QUERY as ACCURACY_QUERY
from modelmind.clients.bigquery.client import BigqueryClient
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.statistics import Accuracy, PersonyStatistics

from .base import Command


class CalculatePersonyStatisticsCommand(Command[None]):
    def __init__(
        self,
        questionnaire_id: str,
        bigquery_client: BigqueryClient,
        questionnaires_dao: QuestionnairesDAO,
    ) -> None:
        self.questionnaire_id = questionnaire_id
        self.bigquery_client = bigquery_client
        self.questionnaires_dao = questionnaires_dao

    async def get_db_questionnaire(self, questionnaire_id: str) -> DBQuestionnaire:
        try:
            return await self.questionnaires_dao.get_from_id(questionnaire_id)
        except Exception as e:
            raise e

    def build_accuracy_query(self, db_questionnaire: DBQuestionnaire) -> str:
        return ACCURACY_QUERY.format(questionnaire_id=db_questionnaire.id)

    def transform_accuracy_query_result(self, rows: RowIterator | _EmptyRowIterator) -> list[Accuracy]:
        accuracy_list = []
        for row in rows:
            accuracy = Accuracy(
                confidence_level=row[0],
                total_predictions=row[2],
                correct_predictions=row[3],
                accuracy_percentage=row[4],
            )
            accuracy_list.append(accuracy)
        return accuracy_list

    async def _run(self) -> None:
        db_questionnaire = await self.get_db_questionnaire(self.questionnaire_id)

        accuracy_query = self.build_accuracy_query(db_questionnaire)
        accuracy_query_job = self.bigquery_client.query(accuracy_query)

        rows = accuracy_query_job.result()

        accuracy = self.transform_accuracy_query_result(rows)

        statistics_data = PersonyStatistics(
            type="persony",
            accuracy=accuracy,
        )

        await self.questionnaires_dao.add_statistics(db_questionnaire.id, statistics_data)
