from typing import Any
from pydantic import BaseModel
from abc import ABC, abstractmethod
from modelmind.models.questions.base import Question
from modelmind.models.results.base import Result


class BaseEngine(BaseModel, ABC):


    def __init__(self, questions: list[Question], *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    async def is_completed(self, current_result: Result) -> bool:
        raise NotImplementedError


    @abstractmethod
    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def build_analytics(self, results: Result) -> Any:
        raise NotImplementedError


class Engine(BaseEngine):

    ...
