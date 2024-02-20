from abc import ABC
from typing import TypeVar
from pydantic import BaseModel



class BaseQuestion(BaseModel, ABC):
    text: str
    language: str



class Question(BaseQuestion):
    pass



