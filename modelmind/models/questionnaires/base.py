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
        questions = await self.engine.infer_next_questions(results, max_questions)
        if shuffle:
            import random

            random.shuffle(questions)
        return questions

    def is_completed(
        self,
        results: Result,
    ) -> bool:
        return self.engine.is_completed(results)

    def get_analytics(self, results: Result) -> list[Analytics]:
        analytics_list = self.engine.get_analytics(results)

        return combine_analytics_to_schema(analytics_list)
