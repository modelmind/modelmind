from typing import List, Optional

from google.cloud.firestore import AsyncCollectionReference, DocumentSnapshot

from modelmind.db.exceptions.questionnaires import DBQuestionnaireNotFound
from modelmind.db.schemas import DBIdentifierUUID
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion
from modelmind.db.utils.type_adapter import TypeAdapter

from .base import FirestoreDAO


class QuestionnairesDAO(FirestoreDAO[DBQuestionnaire]):
    _collection_name = "questionnaires"
    _subcollection_questions = "questions"

    @classmethod
    async def get_from_id(cls, questionnaire_id: DBIdentifierUUID) -> DBQuestionnaire:
        doc: DocumentSnapshot = await cls.collection().document(str(questionnaire_id)).get()
        if doc.exists:
            return DBQuestionnaire.model_validate(doc.to_dict())
        raise DBQuestionnaireNotFound()

    @classmethod
    async def get_from_name(cls, name: str) -> DBQuestionnaire:
        query = cls.collection().where("name", "==", name)
        docs: list[DocumentSnapshot] = await query.get()
        for doc in docs:
            return DBQuestionnaire.model_validate(doc.to_dict())
        raise DBQuestionnaireNotFound()

    @classmethod
    async def get_questions(
        cls, questionnaire_id: DBIdentifierUUID, language: Optional[str] = None
    ) -> List[DBQuestion]:
        questions_ref: AsyncCollectionReference = (
            cls.collection().document(str(questionnaire_id)).collection(cls._subcollection_questions)
        )

        if language:
            questions_ref = questions_ref.where("language", "==", language)

        questions_docs: List[DocumentSnapshot] = await questions_ref.get()
        questions_list = [doc.to_dict() for doc in questions_docs if doc.exists]

        return TypeAdapter.validate(List[DBQuestion], questions_list)

    @classmethod
    async def get_available_languages(cls, questionnaire_id: DBIdentifierUUID) -> List[str]:
        # TODO: optimize this
        questions_ref: AsyncCollectionReference = (
            cls.collection().document(str(questionnaire_id)).collection(cls._subcollection_questions)
        )
        questions_docs: List[DocumentSnapshot] = await questions_ref.get()
        languages = set()
        for doc in questions_docs:
            languages.add(doc.get("language"))
        return list(languages)
