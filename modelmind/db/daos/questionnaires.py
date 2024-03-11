import logging
from typing import Any, AsyncIterator, List, Optional

from google.cloud.firestore import AsyncClient, AsyncCollectionReference, DocumentSnapshot

from modelmind.db.exceptions.questionnaires import DBQuestionnaireNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.questionnaires import CreateQuestionnaire, DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion

from .base import FieldFilter, FirestoreDAO


class QuestionnairesDAO(FirestoreDAO[DBQuestionnaire]):
    _collection_name = "questionnaires"
    model = DBQuestionnaire

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    def questions_collection(self, questionnaire_id: DBIdentifier) -> AsyncCollectionReference:
        return self.document_ref(questionnaire_id).collection("questions")

    async def get_from_id(self, questionnaire_id: DBIdentifier) -> DBQuestionnaire:
        try:
            print("Searching for questionnaire with id", questionnaire_id)
            return await self.get(questionnaire_id)
        except Exception:
            raise DBQuestionnaireNotFound("Questionnaire with id %s not found" % questionnaire_id)

    async def get_from_name(self, name: str) -> DBQuestionnaire:
        try:
            print("Searching for questionnaire with name", name)
            logging.info("Searching for questionnaire with name %s", name)
            return (await self.search([FieldFilter("name", "==", name)], limit=1))[0]
        except Exception:
            raise DBQuestionnaireNotFound("Questionnaire with name %s not found" % name)

    async def get_questions(self, questionnaire_id: DBIdentifier, language: Optional[str] = None) -> List[DBQuestion]:
        questions = self.questions_collection(questionnaire_id)

        if language:
            questions = questions.where("language", "==", language)

        questions_iterator: AsyncIterator[DocumentSnapshot] = questions.stream()

        db_questions: list[DBQuestion] = []
        async for question in questions_iterator:
            db_questions.append(DBQuestion.model_validate({"id": question.id, **question.to_dict()}))

        return db_questions

    async def get_available_languages(self, questionnaire_id: DBIdentifier) -> List[str]:
        # TODO: optimize this, maybe we can store the available languages in the questionnaire document
        questions = self.questions_collection(questionnaire_id)

        questions_iterator: AsyncIterator[DocumentSnapshot] = questions.stream()
        languages = set()
        async for question in questions_iterator:
            languages.add(question.get("language"))
        return list(languages)

    async def create_questionnaire(self, create_questionnaire: CreateQuestionnaire) -> DBQuestionnaire:
        try:
            questionnaire = await self.add(create_questionnaire.model_dump(exclude={"questions"}))
            questions = self.questions_collection(questionnaire.id)

            await self.batch_add(create_questionnaire.questions, questions)

            return questionnaire

        except Exception as e:
            raise e

    async def add_questions(self, questionnaire_id: DBIdentifier, questions: List[dict[str, Any]]) -> None:
        questions_collection = self.questions_collection(questionnaire_id)
        await self.batch_add(questions, questions_collection)
