from pydantic import BaseModel
from abc import ABC

class BaseEngine(BaseModel, ABC):
    ...

