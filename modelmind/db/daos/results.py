from typing import List
from uuid import UUID

from modelmind.db.firestore import firestore_client as db
from modelmind.db.schemas.results import CreateResult, DBResult

from .base import FirestoreDAO


class ResultsDAO(FirestoreDAO[DBResult]):
    _collection_name = "results"

    @classmethod
    async def save(self, result: CreateResult) -> None:
        await db.collection(self.collection_name).document(result.id).set(result.model_dump())

    @classmethod
    async def get_result_from_session_id(self, session_id: UUID) -> DBResult:
        query = db.collection(self.collection_name).where("session_id", "==", session_id)
        docs = await query.get()
        return DBResult.model_validate(docs[0].to_dict())

    @classmethod
    async def get_results_from_questionnaire(self, questionnaire_id: UUID, limit: int) -> List[DBResult]:
        query = (
            db.collection(self.collection_name)
            .where("questionnaire_id", "==", questionnaire_id)
            .order_by("created_at", direction="DESCENDING")
            .limit(limit)
        )
        docs = await query.get()
        return [DBResult.model_validate(doc.to_dict()) for doc in docs]

    @classmethod
    async def get_result_from_id(self, result_id: UUID) -> DBResult:
        doc = await db.collection(self.collection_name).document(str(result_id)).get()
        return DBResult.model_validate(doc.to_dict())
