from abc import ABC, abstractmethod

from pydantic import BaseModel
from modelmind.models.engines.base import BaseEngine, Engine
from modelmind.models.questions.base import BaseQuestion, Question
from modelmind.models.results.base import BaseResult, Result
from modelmind.models.analytics.base import BaseAnalytics, Analytics
from typing import TypeVar, Generic

QuestionType = TypeVar('QuestionType', bound=BaseQuestion)
EngineType = TypeVar('EngineType', bound=BaseEngine)
ResultType = TypeVar('ResultType', bound=BaseResult)

class BaseQuestionnaire(BaseModel, Generic[QuestionType, EngineType, ResultType], ABC):

    name: str
    engine: EngineType
    questions: list[QuestionType]

    def __init__(self, name: str, engine: EngineType, questions: list[QuestionType]) -> None:
        self.name = name
        self.engine = engine
        self.questions = questions

    @abstractmethod
    async def next_questions(
        self,
        results: ResultType,
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
        pass

    async def next_questions(
        self,
        results: Result,
    ) -> list[Question]:
        return await self.engine.infer_next_questions(results)

    def is_completed(
        self,
        results: Result,
    ) -> bool:
        return self.engine.is_completed(results)

    def get_analytics(self, results: Result) -> list[Analytics]:
        analytics_list = self.engine.get_analytics(results)

        return Analytics.combine(analytics_list)
