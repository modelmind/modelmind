from abc import ABC, abstractproperty
from pydantic import BaseModel


from typing import Union, Literal
from pydantic import BaseModel, Field

KEY_DELIMITER = '#'

QuestionKey = str

class BaseQuestion(BaseModel, ABC):

    @abstractproperty
    def key(self) -> QuestionKey:
        raise NotImplementedError


class ChoiceQuestion(BaseQuestion):
    type: Literal['choiceQuestion']
    text: str
    multiple: bool
    display: Literal['radio', 'checkbox', 'dropdown']
    options: list
    shuffle: bool


class TextQuestion(BaseQuestion):
    type: Literal['textQuestion']
    text: str


class ScaleQuestion(BaseQuestion):
    type: Literal['scaleQuestion']
    text: str
    min: int
    max: int
    interval: float
    lowLabel: str
    highLabel: str


class Question(BaseModel):
    id: str
    category: str
    question: Union[ChoiceQuestion, TextQuestion, ScaleQuestion] = Field(..., discriminator='type')

    language: str | None = None
    required: bool = True

    @property
    def key(self) -> QuestionKey:
        return f"{self.category}{KEY_DELIMITER}{self.id}"


