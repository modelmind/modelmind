from typing import List, Optional
from uuid import UUID

from .base import FirestoreDAO
from modelmind.services.firestore import firestore_client as db
from modelmind.db.schemas.firestore import Document


class QuestionnairesDAO(FirestoreDAO):
    collection_name = "questionnaires"

    @classmethod
    async def get(self, questionnaire_id: UUID) -> None:
        ...

    @classmethod
    async def get_questions(self, questionnaire_id: UUID, language: Optional[str]) -> List[Document]:
        doc_ref = db.collection(self.collection_name).document(str(questionnaire_id))
        doc = await doc_ref.get()
        if doc.exists:
            return doc.to_dict().get("questions")
        else:
            return []
