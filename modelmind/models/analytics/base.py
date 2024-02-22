from abc import ABC
from pydantic import BaseModel


class BaseAnalytics(BaseModel, ABC):
    ...


