from datetime import datetime
from typing import Any, AsyncIterator, List, Literal, Optional

from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer
from google.cloud.firestore import AsyncClient, AsyncCollectionReference, DocumentSnapshot
from google.cloud.firestore_v1.types import write
from shortuuid import uuid

from modelmind.db.exceptions.questionnaires import DBQuestionnaireNotFound
from modelmind.db.schemas import DBIdentifier
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.questions import DBQuestion
from modelmind.db.schemas.statistics import StatisticsData
from modelmind.logger import log

from .base import FieldFilter, FirestoreDAO


class QuestionnairesDAO(FirestoreDAO[DBQuestionnaire]):
    _collection_name = "questionnaires"
    model = DBQuestionnaire

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    def questions_collection(self, questionnaire_id: DBIdentifier) -> AsyncCollectionReference:
        return self.document_ref(questionnaire_id).collection("questions")

    def statistics_collection(self, questionnaire_id: DBIdentifier) -> AsyncCollectionReference:
        return self.document_ref(questionnaire_id).collection("statistics")

    @cached(ttl=3600, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def get_from_id(self, questionnaire_id: DBIdentifier) -> DBQuestionnaire:
        try:
            log.info("Searching for questionnaire with id %s", questionnaire_id)
            return await self.get(questionnaire_id)
        except Exception:
            raise DBQuestionnaireNotFound("Questionnaire with id %s not found" % questionnaire_id)

    @cached(ttl=3600, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def get_from_name(self, name: str) -> DBQuestionnaire:
        try:
            log.info("Searching for questionnaire with name %s", name)
            return (await self.search([FieldFilter("name", "==", name)], limit=1))[0]
        except Exception:
            raise DBQuestionnaireNotFound("Questionnaire with name %s not found" % name)

    @cached(ttl=900, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def get_questions(self, questionnaire_id: DBIdentifier, language: Optional[str] = None) -> List[DBQuestion]:
        questions = self.questions_collection(questionnaire_id)

        if language:
            questions = questions.where("language", "==", language)

        questions_iterator: AsyncIterator[DocumentSnapshot] = questions.stream()

        db_questions: list[DBQuestion] = []
        async for question in questions_iterator:
            db_questions.append(DBQuestion.model_validate({"id": question.id, **question.to_dict()}))

        return db_questions

    @cached(ttl=300, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def get_available_languages(self, questionnaire_id: DBIdentifier) -> List[str]:
        # TODO: optimize this, maybe we can store the available languages in the questionnaire document
        questions = self.questions_collection(questionnaire_id)

        questions_iterator: AsyncIterator[DocumentSnapshot] = questions.stream()
        languages = set()
        async for question in questions_iterator:
            languages.add(question.get("language"))
        return list(languages)

    @cached(ttl=300, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def is_language_available(self, questionnaire_id: DBIdentifier, language: str) -> bool:
        """Check if questionnaire has at least one question in specified language."""
        questions = self.questions_collection(questionnaire_id).where("language", "==", language).limit(1)
        async for _ in questions.stream():
            return True
        return False

    async def create_questionnaire(
        self,
        name: str,
        engine: str,
        config: dict,
        questions: List[dict[str, Any]],
        owner: str,
        visibility: Literal["public", "private"],
        description: str = "",
    ) -> DBQuestionnaire:
        try:
            # TODO: maybe we should bypass cache here
            await self.get_from_name(name)
            raise ValueError("Questionnaire with name %s already exists" % name)
        except DBQuestionnaireNotFound:
            pass

        questionnare_id = str(uuid()[:8])

        questionnaire_data = {
            "id": questionnare_id,
            "name": name,
            "description": description,
            "engine": engine,
            "config": config,
            "owner": owner,
            "visibility": visibility,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        try:
            questionnaire = await self.add(questionnaire_data, questionnare_id)
            questions_collection_ref = self.questions_collection(questionnaire.id)

            doc_ids = [
                self.build_question_doc_id(questionnaire.id, question["id"], question["language"])
                for question in questions
            ]
            for question in questions:
                question["questionnaire_id"] = questionnaire.id

            await self.batch_add(questions, questions_collection_ref, doc_ids)

            return questionnaire

        except Exception as e:
            raise e

    async def add_questions(self, questionnaire_id: DBIdentifier, questions: List[dict[str, Any]]) -> None:
        doc_ids = [
            self.build_question_doc_id(questionnaire_id, question["id"], question["language"]) for question in questions
        ]
        for question in questions:
            question["questionnaire_id"] = questionnaire_id

        questions_collection = self.questions_collection(questionnaire_id)
        await self.batch_add(questions, questions_collection, doc_ids)

    async def update_question(self, questionnaire_id: DBIdentifier, question: dict[str, Any]) -> None:
        question_ref = self.questions_collection(questionnaire_id).document(
            self.build_question_doc_id(questionnaire_id, question["id"], question["language"])
        )
        write_result: write.WriteResult = await question_ref.update(question)
        log.debug(
            f"Question {question["id"]} from questionnaire {questionnaire_id} updated at {write_result.update_time}"
        )

    async def add_statistics(self, questionnaire_id: DBIdentifier, statistics_data: StatisticsData) -> None:
        statistics_collection = self.statistics_collection(questionnaire_id)
        statistics_document = {
            "questionnaire_id": questionnaire_id,
            "created_at": datetime.now(),
            "data": statistics_data,
        }
        await statistics_collection.add(statistics_document)

    @staticmethod
    def build_question_doc_id(questionnaire_id: DBIdentifier, question_id: str, language: str) -> str:
        return f"{questionnaire_id}_{question_id}_{language}"
