from abc import ABC, abstractproperty
from pydantic import BaseModel

QuestionKey = str

SimpleQuestionKey = str

class BaseQuestion(BaseModel, ABC):

    text: str
    value: str

    language: str

    @property
    def is_answered(self) -> bool:
        return self.value is not None

    @abstractproperty
    def key(self) -> QuestionKey:
        raise NotImplementedError


class SimpleQuestion(BaseQuestion):

    @property
    def key(self) -> SimpleQuestionKey:
        return f"{self.text}.{self.language}"



class OppositeQuestion(BaseQuestion):

    left_side: str
    right_side: str

    @property
    def key(self) -> SimpleQuestionKey:
        return f"{self.text}.{self.language}"

