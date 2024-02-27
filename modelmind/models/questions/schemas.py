from typing import Literal, Union

from pydantic import BaseModel, Field

KEY_DELIMITER = "#"

QuestionID = str
QuestionKey = str
QuestionCategory = str


class ChoiceQuestion(BaseModel):
    type: Literal["choice"]
    text: str
    multiple: bool
    display: Literal["radio", "checkbox", "dropdown"]
    options: list
    shuffle: bool


class TextQuestion(BaseModel):
    type: Literal["text"]
    text: str


class ScaleQuestion(BaseModel):
    type: Literal["scale"]
    text: str
    min: int
    max: int
    interval: float
    low_label: str
    high_label: str


class Question(BaseModel):
    id: QuestionID
    category: QuestionCategory
    question: Union[ChoiceQuestion, TextQuestion, ScaleQuestion] = Field(..., discriminator="type")

    language: str
    required: bool = True

    @property
    def key(self) -> QuestionKey:
        return f"{self.category}{KEY_DELIMITER}{self.id}"
