from abc import ABC, abstractmethod
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class BaseAnalytics(ABC):
    class BaseItem(BaseModel):
        ...

    items: list

    @abstractmethod
    def to_analytics_representation(self) -> "Analytics":
        raise NotImplementedError


class Analytics(BaseAnalytics):
    # TODO: Add support for more item types
    # TODO: may change extra to a more specific type
    class ScoreItem(BaseAnalytics.BaseItem):
        type: Literal["score"] = "score"
        name: str
        value: int | float
        percentage: Optional[float] = None
        categories: list[str] = []

    name: str
    items: list[Union[ScoreItem]] = Field(..., discriminator="type")
    extra: dict

    @classmethod
    def combine(cls, analytics: list[Union[BaseAnalytics, "Analytics"]]) -> list["Analytics"]:
        return [analytic.to_analytics_representation() for analytic in analytics]

    def to_analytics_representation(self) -> "Analytics":
        return self

    @property
    def categories(self) -> list[str]:
        return list(set([category for item in self.items for category in item.categories]))
