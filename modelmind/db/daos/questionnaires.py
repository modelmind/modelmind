from typing import AsyncIterator, List, Optional

from google.cloud.firestore import AsyncCollectionReference, DocumentSnapshot

from modelmind.db.exceptions.questionnaires import DBQuestionnaireNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion

from .base import FieldFilter, FirestoreDAO


class QuestionnairesDAO(FirestoreDAO[DBQuestionnaire]):
    _collection_name = "questionnaires"

    @classmethod
    def questions_collection(self, questionnaire_id: DBIdentifier) -> AsyncCollectionReference:
        return self.document_ref(questionnaire_id).collection("questions")

    @classmethod
    async def get_from_id(self, questionnaire_id: DBIdentifier) -> DBQuestionnaire:
        try:
            return await self.get(questionnaire_id)
        except Exception:
            raise DBQuestionnaireNotFound()

    @classmethod
    async def get_from_name(self, name: str) -> DBQuestionnaire:
        try:
            return (await self.search([FieldFilter("name", "==", name)], limit=1))[0]
        except Exception:
            raise DBQuestionnaireNotFound()

    @classmethod
    async def get_questions(self, questionnaire_id: DBIdentifier, language: Optional[str] = None) -> List[DBQuestion]:
        questions = self.questions_collection(questionnaire_id)

        if language:
            questions = questions.where("language", "==", language)

        questions_iterator: AsyncIterator[DocumentSnapshot] = await questions.stream()

        db_questions: list[DBQuestion] = []
        async for question in questions_iterator:
            db_questions.append(DBQuestion.model_validate({"id": question.id, **question.to_dict()}))

        return db_questions

    @classmethod
    async def get_available_languages(self, questionnaire_id: DBIdentifier) -> List[str]:
        # TODO: optimize this, maybe we can store the available languages in the questionnaire document
        questions = self.questions_collection(questionnaire_id)

        questions_iterator: AsyncIterator[DocumentSnapshot] = await questions.stream()
        languages = set()
        async for question in questions_iterator:
            languages.add(question.get("language"))
        return list(languages)
