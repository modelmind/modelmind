from abc import ABC, abstractmethod

from .schemas import Analytics


class BaseAnalytics(ABC):
    @abstractmethod
    def to_schema(self) -> "Analytics":
        raise NotImplementedError
