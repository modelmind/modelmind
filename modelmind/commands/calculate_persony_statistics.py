from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator

from bigquery.queries.calculate_accuracy import QUERY as ACCURACY_QUERY
from bigquery.queries.results_counts import QUERY as COUNTS_QUERY
from modelmind.clients.bigquery.client import BigqueryClient
from modelmind.db.daos.questionnaires import QuestionnairesDAO
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.statistics import Accuracy, AccuracyMetric, CountsMetric, PersonyStatistics

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

    def build_counts_query(self, db_questionnaire: DBQuestionnaire) -> str:
        return COUNTS_QUERY.format(questionnaire_id=db_questionnaire.id)

    def transform_accuracy_query_result(self, rows: RowIterator | _EmptyRowIterator) -> AccuracyMetric:
        data = list(rows)

        return AccuracyMetric(
            total=Accuracy(
                total_predictions=data[0][2],
                correct_predictions=data[0][3],
                percentage=data[0][4],
            ),
            confidence_ge_1=Accuracy(
                total_predictions=data[1][2],
                correct_predictions=data[1][3],
                percentage=data[1][4],
            ),
            confidence_ge_2=Accuracy(
                total_predictions=data[2][2],
                correct_predictions=data[2][3],
                percentage=data[2][4],
            ),
            confidence_ge_3=Accuracy(
                total_predictions=data[3][2],
                correct_predictions=data[3][3],
                percentage=data[3][4],
            ),
            confidence_ge_4=Accuracy(
                total_predictions=data[4][2],
                correct_predictions=data[4][3],
                percentage=data[4][4],
            ),
        )

    def transform_counts_query_result(self, rows: RowIterator | _EmptyRowIterator) -> CountsMetric:
        data = list(rows)
        return CountsMetric(
            total=data[0][0],
            with_label=data[0][1],
            male=data[0][2],
            female=data[0][3],
            other=data[0][4],
        )

    async def _run(self) -> None:
        db_questionnaire = await self.get_db_questionnaire(self.questionnaire_id)

        accuracy_query = self.build_accuracy_query(db_questionnaire)
        accuracy_query_job = self.bigquery_client.query(accuracy_query)

        rows = accuracy_query_job.result()

        accuracy = self.transform_accuracy_query_result(rows)

        counts_query = self.build_counts_query(db_questionnaire)
        counts_query_job = self.bigquery_client.query(counts_query)

        counts_rows = counts_query_job.result()

        counts = self.transform_counts_query_result(counts_rows)

        statistics_data = PersonyStatistics(
            type="persony",
            accuracy=accuracy,
            counts=counts,
        )

        await self.questionnaires_dao.add_statistics(db_questionnaire.id, statistics_data)
