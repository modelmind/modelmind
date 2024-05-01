from enum import StrEnum
from typing import List

from modelmind.models.analytics.base import Analytics, BaseAnalytics


class JungFunction(StrEnum):
    Ni = "Ni"
    Ne = "Ne"
    Si = "Si"
    Se = "Se"
    Ti = "Ti"
    Te = "Te"
    Fi = "Fi"
    Fe = "Fe"

    @classmethod
    def list(cls) -> List[str]:
        return [func.value for func in cls]


class JungFunctionsAnalytics(BaseAnalytics):
    Ni: int = 0
    Ne: int = 0
    Si: int = 0
    Se: int = 0
    Ti: int = 0
    Te: int = 0
    Fi: int = 0
    Fe: int = 0

    def __init__(self) -> None:
        self.values = {func: 0 for func in JungFunction}
        self.max_values = {func: 0 for func in JungFunction}

    @property
    def global_percentages(self) -> dict[str, float]:
        total = sum(self.values.values())
        if total == 0:
            return {func.name: 0 for func in JungFunction}
        return {func.name: (self.values[func] / total) * 100 for func in JungFunction}

    @property
    def percentages(self) -> dict[str, float]:
        return {
            func.name: (self.values[func] / self.max_values[func] * 100 if self.max_values[func] > 0 else 0)
            for func in JungFunction
        }

    def add(self, function: JungFunction, value: int, max_value: int) -> None:
        if function in JungFunction:
            self.values[function] += value
            if max_value > self.max_values[function]:
                self.max_values[function] = max_value

    @property
    def categories(self) -> dict[JungFunction, List[str]]:
        return {
            JungFunction.Ni: ["intuition", "introverted", "irrational"],
            JungFunction.Ne: ["intuition", "extroverted", "irrational"],
            JungFunction.Si: ["sensing", "introverted", "irrational"],
            JungFunction.Se: ["sensing", "extroverted", "irrational"],
            JungFunction.Ti: ["thinking", "introverted", "rational"],
            JungFunction.Te: ["thinking", "extroverted", "rational"],
            JungFunction.Fi: ["feeling", "introverted", "rational"],
            JungFunction.Fe: ["feeling", "extroverted", "rational"],
        }

    def to_schema(self) -> "Analytics":
        items = [
            Analytics.ScoreItem(
                name=func.value,
                value=self.values[func],
                percentage=self.percentages[func.value],
                categories=self.categories[func],
            )
            for func in JungFunction
        ]

        extra = {
            "global_percentages": self.global_percentages,
            "max_values": self.max_values,
        }

        return Analytics(
            name=self.__class__.__name__,
            items=items,
            extra=extra,
        )
