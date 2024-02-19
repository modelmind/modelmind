from abc import ABC
from typing import Any, Generic, TypeVar
from pydantic import Field


QuestionKey = TypeVar("QuestionKey", bound=str)

ResultData = dict[QuestionKey, Any]


class BaseResult(Generic[QuestionKey], ABC):

    data: ResultData = Field(default_factory=dict)

    def __init__(self, **kwargs):
        pass

    def is_empty(self) -> bool:
        return not bool(self.data)

    def count_answered_questions(self) -> int:
        return len([v for v in self.data.values() if v is not None])

    def get_answered_questions(self) -> list[QuestionKey]:
        return [k for k, v in self.data.items() if v is not None]
