from abc import ABC
from typing import Any, Generic, TypeVar
from pydantic import Field


QuestionKey = TypeVar("QuestionKey", bound=str)

ResultData = dict[QuestionKey, Any]


class BaseResult(Generic[QuestionKey], ABC):

    data: ResultData = Field(default_factory=dict)

    def __init__(self, data: ResultData, **kwargs):
        self.data = data or {}

    def is_empty(self) -> bool:
        return not bool(self.data)

    def count_answered_questions(self) -> int:
        return len([v for v in self.data.values() if v is not None])

    def list_answered_questions_keys(self) -> list[QuestionKey]:
        return [k for k, v in self.data.items() if v is not None]



class Result(BaseResult[str]):

    def __init__(self, data: ResultData, **kwargs):
        super().__init__(data=data, **kwargs)

