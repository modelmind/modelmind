from typing import Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
from modelmind.models.questions.base import BaseQuestion
from modelmind.models.results.base import BaseResult


class BaseEngine(BaseModel, ABC):
    ...



class SimpleEngine(BaseEngine, ABC):

    def __init__(self, questions: list[BaseQuestion]) -> None:
        self.questions = questions

    async def infer_next_questions(self, result: BaseResult, max_questions: Optional[int] = None) -> list[BaseQuestion]:
        answered_questions_keys = result.get_answered_questions()
        remaining_questions = [q for q in self.questions if q.key not in answered_questions_keys]
        return remaining_questions[:max_questions]


class AdaptiveEngine(BaseEngine, ABC):

    def __init__(self, questions: list[BaseQuestion]) -> None:
        self.questions = questions

    @property
    def current_step(self) -> int:
        return 0

    async def infer_next_questions(self, result: BaseResult, max_questions: Optional[int] = None) -> list[BaseQuestion]:
        return []
