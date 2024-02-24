from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, TypeVar

from pydantic import BaseModel

from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.questions.base import Question
from modelmind.models.results.base import QuestionKey, Result

QuestionType = TypeVar("QuestionType", bound=Question)


class BaseEngine(BaseModel, Generic[QuestionType], ABC):
    def __init__(self, questions: list[QuestionType], *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def is_completed(self, current_result: Result) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        raise NotImplementedError


class Engine(BaseEngine, Generic[QuestionType]):
    def __init__(self, questions: list[QuestionType], *args: Any, **kwargs: Any) -> None:
        super().__init__(questions, *args, **kwargs)
        self._analytics: list[BaseAnalytics] = []
        self.question_key_mapping: Dict[QuestionKey, QuestionType] = self._createquestion_key_mapping(questions)

    def _createquestion_key_mapping(self, questions: List[QuestionType]) -> Dict[QuestionKey, QuestionType]:
        """Preprocess the questions list to create a key to question mapping."""
        return {question.key: question for question in questions}

    def is_completed(self, current_result: Result) -> bool:
        return current_result.is_empty()

    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        return []

    def _build_analytics(self, results: Result) -> list[BaseAnalytics]:
        return []

    def get_analytics(self, results: Result) -> list[BaseAnalytics]:
        if not self._analytics:
            self._analytics = self._build_analytics(results)
        return self._analytics
