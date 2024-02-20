from abc import ABC, abstractmethod
from modelmind.models.engines.base import BaseEngine
from modelmind.models.questions.base import BaseQuestion
from modelmind.models.results.base import BaseResult


class BaseQuestionnaire(ABC):

    name: str
    engine: BaseEngine
    questions: list[BaseQuestion]

    def __init__(self, name: str, engine: BaseEngine, questions: list[BaseQuestion]) -> None:
        self.name = name
        self.engine = engine
        self.questions = questions

    @abstractmethod
    async def next_questions(
        self,
        results: BaseResult,
    ) -> list[BaseQuestion]:
        raise NotImplementedError

    @abstractmethod
    async def is_questionnaire_completed(
        self,
        results: BaseResult,
    ) -> bool:
        raise NotImplementedError


class Questionnaire(BaseQuestionnaire):

    def __init__(self, name: str, engine: BaseEngine, questions: list[BaseQuestion]) -> None:
        super().__init__(name, engine, questions)

    async def next_questions(
        self,
        results: BaseResult,
    ) -> list[BaseQuestion]:
        return await self.engine.infer_next_questions(self.questions, results)

    async def is_questionnaire_completed(
        self,
        results: BaseResult,
    ) -> bool:
        return False
