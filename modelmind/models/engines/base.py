from pydantic import BaseModel
from abc import ABC, abstractmethod
from modelmind.models.questions.base import Question
from modelmind.models.results.base import Result


class BaseEngine(BaseModel, ABC):

    def __init__(self, questions: list[Question]) -> None:
        self.questions = questions

    @abstractmethod
    async def infer_next_questions(self, current_result: Result) -> list[Question]:
        raise NotImplementedError


class Engine(BaseEngine):

    ...

