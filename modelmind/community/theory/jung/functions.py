import math
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
        pass

    @staticmethod
    def _softmax(x: List[int]) -> List[float]:
        """Compute softmax values for each sets of scores in x."""
        e_x = [math.exp(i) for i in x]
        return [i / sum(e_x) for i in e_x]

    @property
    def model_fields(self) -> List[str]:
        return [str(func) for func in JungFunction]

    @property
    def normalized_functions(self) -> dict[str, float]:
        function_values = [
            self.Ni,
            self.Ne,
            self.Si,
            self.Se,
            self.Ti,
            self.Te,
            self.Fi,
            self.Fe,
        ]
        softmax_values = self._softmax(function_values)

        return {
            "Ni": softmax_values[0] * 100,
            "Ne": softmax_values[1] * 100,
            "Si": softmax_values[2] * 100,
            "Se": softmax_values[3] * 100,
            "Ti": softmax_values[4] * 100,
            "Te": softmax_values[5] * 100,
            "Fi": softmax_values[6] * 100,
            "Fe": softmax_values[7] * 100,
        }

    @property
    def percentages(self) -> dict[str, float]:
        total = sum(getattr(self, func) for func in self.model_fields)
        return {func: (getattr(self, func) / total) * 100 for func in self.model_fields}

    def add(self, function: JungFunction, value: int) -> None:
        if function in self.model_fields:
            setattr(self, function, getattr(self, function) + value)

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
                value=getattr(self, func.value),
                percentage=self.percentages[func.value],
                categories=self.categories[func],
            )
            for func in JungFunction
        ]

        extra = {
            "percentages": self.percentages,
            "normalized_functions": self.normalized_functions,
        }

        return Analytics(
            name=self.__class__.__name__,
            items=items,
            extra=extra,
        )
