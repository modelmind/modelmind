from pydantic import BaseModel
from abc import ABC, abstractmethod
from models.questions.base import BaseQuestion
from models.results.base import BaseResult


class BaseEngine(BaseModel, ABC):

    def __init__(self, questions: list[BaseQuestion]) -> None:
        self.questions = questions

    @abstractmethod
    async def infer_next_questions(self, current_result: BaseResult) -> list[BaseQuestion]:
        raise NotImplementedError


class Engine(BaseEngine):

    ...

