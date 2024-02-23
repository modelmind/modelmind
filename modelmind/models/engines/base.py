from typing import Any
from pydantic import BaseModel
from abc import ABC, abstractmethod
from modelmind.models.questions.base import Question
from modelmind.models.results.base import Result
from modelmind.models.analytics.base import BaseAnalytics


class BaseEngine(BaseModel, ABC):


    def __init__(self, questions: list[Question], *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def is_completed(self, current_result: Result) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        raise NotImplementedError



class Engine(BaseEngine):

    def __init__(self, questions: list[Question], *args: Any, **kwargs: Any) -> None:
        super().__init__(questions, *args, **kwargs)
        self._analytics: list[BaseAnalytics] = []

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
