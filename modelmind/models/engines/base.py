from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Any, TypeVar

Question = TypeVar('Question', bound=Any)
Result = TypeVar('Result', bound=Any)

class BaseEngine(BaseModel, ABC):

    def __init__(self, questions: list[Question]) -> None:
        self.questions = questions

    @abstractmethod
    async def infer_next_questions(self, questions: list[Question], current_result: Result) -> list[Question]:
        raise NotImplementedError


class Engine(BaseEngine):

    ...

