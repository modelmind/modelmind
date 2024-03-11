from typing import List, Optional

from google.cloud.firestore import AsyncClient

from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.results import CreateResult, DBResult, UpdateResultVisibility

from .base import FieldFilter, FirestoreDAO


class ResultsDAO(FirestoreDAO[DBResult]):
    _collection_name = "results"
    model = DBResult

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    async def save(self, result: CreateResult) -> DBResult:
        try:
            return await self.add(result.model_dump())
        except Exception as e:
            # TODO: custom exception
            raise e

    async def get_result_from_session_id(self, session_id: DBIdentifier) -> DBResult:
        try:
            return (await self.search(filters=[FieldFilter("session_id", "==", session_id)], limit=1))[0]
        except Exception as e:
            # TODO: custom exception
            raise e

    async def get_results_from_questionnaire(
        self, questionnaire_id: DBIdentifier, limit: Optional[int] = None
    ) -> List[DBResult]:
        try:
            return await self.search(filters=[FieldFilter("questionnaire_id", "==", questionnaire_id)], limit=limit)
        except Exception as e:
            # TODO: custom exception
            raise e

    async def get_from_id(self, result_id: DBIdentifier) -> DBResult:
        try:
            return await self.get(result_id)
        except Exception as e:
            # TODO: custom exception
            raise e

    async def update_visibility(self, result_id: DBIdentifier, data: UpdateResultVisibility) -> None:
        try:
            await self.update(result_id, data.model_dump())
        except Exception as e:
            # TODO: custom exception
            raise e
