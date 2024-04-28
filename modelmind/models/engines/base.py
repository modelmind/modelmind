from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.questions.schemas import Question
from modelmind.models.results.base import QuestionKey, Result

QuestionType = TypeVar("QuestionType", bound=Question)


class BaseEngine(Generic[QuestionType], ABC):
    question_key_mapping: Dict[QuestionKey, QuestionType]

    def __init__(self, questions: list[QuestionType]) -> None:
        self.question_key_mapping: Dict[QuestionKey, QuestionType] = self._createquestion_key_mapping(questions)
        super().__init__()

    def _createquestion_key_mapping(self, questions: List[QuestionType]) -> Dict[QuestionKey, QuestionType]:
        """Create a mapping question_key to -> Question"""
        return {question.key: question for question in questions}

    @abstractmethod
    def is_completed(self, current_result: Result) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def infer_next_questions(
        self, current_result: Result, max_questions: Optional[int], shuffle: bool = True
    ) -> list[Question]:
        raise NotImplementedError


class Engine(BaseEngine, Generic[QuestionType]):
    _analytics: list[BaseAnalytics]

    def __init__(self, questions: list[QuestionType], config: Optional[Any] = None) -> None:
        super().__init__(questions)
        self._analytics: list[BaseAnalytics] = []

    def is_completed(self, current_result: Result) -> bool:
        return current_result.is_empty()

    async def infer_next_questions(
        self, current_result: Result, max_questions: Optional[int], shuffle: bool = True
    ) -> list[Question]:
        return []

    def build_analytics(self, results: Result) -> list[BaseAnalytics]:
        return []

    def get_analytics(self, results: Result) -> list[BaseAnalytics]:
        if not self._analytics:
            self._analytics = self.build_analytics(results)
        return self._analytics

    def calculate_result_label(self, results: Result) -> str:
        return ""

    async def calculate_remaining_questions_count(self, results: Result) -> int:
        return 0
