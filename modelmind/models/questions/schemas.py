from abc import ABC
from typing import Literal, Union

from pydantic import BaseModel, Field

QuestionID = str
QuestionKey = str
QuestionCategory = str
AnswerType = Literal["string", "array", "map", "boolean", "number", "timestamp", "geopoint"]


class QuestionType(BaseModel, ABC):
    type: Literal["choice", "text", "scale"]
    answer_type: AnswerType = "string"


class ChoiceQuestion(QuestionType):
    type: Literal["choice"]
    text: str
    multiple: bool
    display: Literal["radio", "checkbox", "dropdown"]
    options: list
    shuffle: bool
    answer_type: AnswerType = "string"


class TextQuestion(QuestionType):
    type: Literal["text"]
    text: str
    answer_type: AnswerType = "string"


class ScaleQuestion(QuestionType):
    type: Literal["scale"]
    text: str
    min: int
    max: int
    interval: float
    low_label: str
    high_label: str
    shuffle: bool = True
    reversed: bool = False
    answer_type: AnswerType = "number"


class Question(BaseModel):
    id: QuestionID
    category: QuestionCategory
    question: Union[ChoiceQuestion, TextQuestion, ScaleQuestion] = Field(..., discriminator="type")

    language: str
    required: bool = True

    @property
    def key(self) -> QuestionKey:
        return f"{self.id}"
