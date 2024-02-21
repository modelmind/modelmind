from typing import List, Optional

from google.cloud.firestore import AsyncCollectionReference, DocumentSnapshot

from db.utils.type_adapter import TypeAdapter

from .base import FirestoreDAO
from db.schemas import DBIdentifierUUID
from db.schemas.questions import DBQuestion
from db.schemas.questionnaires import DBQuestionnaire
from db.exceptions.questionnaires import QuestionnaireNotFound


class QuestionnairesDAO(FirestoreDAO[DBQuestionnaire]):
    _collection_name = "questionnaires"

    @classmethod
    async def get_by_name(cls, name: str) -> DBQuestionnaire:
        query = cls.collection().where("name", "==", name)
        docs: list[DocumentSnapshot] = await query.get()
        for doc in docs:
            return DBQuestionnaire.model_validate(doc.to_dict())
        raise QuestionnaireNotFound()


    @classmethod
    async def get_questions(cls, questionnaire_id: DBIdentifierUUID, language: Optional[str] = None) -> List[DBQuestion]:
        questions_ref: AsyncCollectionReference = cls.collection().document(str(questionnaire_id)).collection('questions')

        if language:
            questions_ref = questions_ref.where('language', '==', language)

        questions_docs: List[DocumentSnapshot] = await questions_ref.get()
        questions_list = [doc.to_dict() for doc in questions_docs if doc.exists]

        return TypeAdapter.validate(List[DBQuestion], questions_list)

