from enum import StrEnum
import math
from typing import List
from modelmind.models.analytics.base import BaseAnalytics


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

    @staticmethod
    def _softmax(x: List[int]) -> List[float]:
        """Compute softmax values for each sets of scores in x."""
        e_x = [math.exp(i) for i in x]
        return [i / sum(e_x) for i in e_x]

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
