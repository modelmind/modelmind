from typing import Any
from pydantic import Field
from .base import BaseResult


ResultData = dict[PersonyQuestionCategory, Any]

class PersonyResult(BaseResult):

    data: dict = Field(default_factory=dict)

    def __init__(self, **kwargs):
        pass

    def get_results(self):
        raise NotImplementedError



