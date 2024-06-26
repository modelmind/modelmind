from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from modelmind.models.analytics.base import Analytics
from modelmind.models.analytics.transformations import combine_analytics_to_schema
from modelmind.models.engines.base import BaseEngine, Engine
from modelmind.models.questions.schemas import Question
from modelmind.models.results.base import BaseResult, Result

QuestionType = TypeVar("QuestionType", bound=Question)
EngineType = TypeVar("EngineType", bound=BaseEngine)
ResultType = TypeVar("ResultType", bound=BaseResult)


class BaseQuestionnaire(Generic[QuestionType, EngineType, ResultType], ABC):
    name: str
    engine: EngineType
    questions: list[QuestionType]

    def __init__(self, name: str, engine: EngineType, questions: list[QuestionType]) -> None:
        self.name = name
        self.engine = engine
        self.questions = questions

    @abstractmethod
    async def next_questions(
        self, results: ResultType, max_questions: Optional[int] = None, shuffle: bool = True
    ) -> list[QuestionType]:
        raise NotImplementedError

    @abstractmethod
    def is_completed(
        self,
        results: ResultType,
    ) -> bool:
        raise NotImplementedError


class Questionnaire(BaseQuestionnaire[Question, Engine, Result]):
    def __init__(self, name: str, engine: Engine, questions: list[Question]) -> None:
        super().__init__(name, engine, questions)

    async def next_questions(
        self, results: Result, max_questions: Optional[int] = None, shuffle: bool = True
    ) -> list[Question]:
        return await self.engine.infer_next_questions(results, max_questions, shuffle)

    def is_completed(
        self,
        results: Result,
    ) -> bool:
        return self.engine.is_completed(results)

    def get_analytics(self, results: Result) -> list[Analytics]:
        analytics_list = self.engine.get_analytics(results)

        return combine_analytics_to_schema(analytics_list)

    def get_result_label(self, results: Result) -> str:
        return self.engine.calculate_result_label(results)

    async def get_remaining_questions_count(self, results: Result) -> int:
        return await self.engine.calculate_remaining_questions_count(results)
