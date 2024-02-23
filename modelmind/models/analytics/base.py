from abc import ABC, abstractmethod
from typing import Optional, Union
from pydantic import BaseModel


class BaseAnalytics(BaseModel, ABC):

    class BaseItem(BaseModel):
        ...

    items: list

    @abstractmethod
    def to_analytics_representation(self) -> "Analytics":
        raise NotImplementedError



class Analytics(BaseAnalytics):

    class Item(BaseAnalytics.BaseItem):
        name: str
        value: int | float | str
        percentage: Optional[float] = None
        category: Optional[str] = None

    name: str
    items: list[Item]
    extra: dict

    @classmethod
    def combine(cls, analytics: list[Union[BaseAnalytics, "Analytics"]]) -> list["Analytics"]:
        return [
            analytic.to_analytics_representation()
            for analytic in analytics
        ]

    def to_analytics_representation(self) -> "Analytics":
        return self

    @property
    def categories(self) -> list[str]:
        return list(set([item.category for item in self.items if item.category is not None]))



