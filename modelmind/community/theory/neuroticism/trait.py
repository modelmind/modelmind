from enum import StrEnum

from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.analytics.schemas import Analytics


class NeuroticismTrait(StrEnum):
    N1 = "N1"
    S1 = "S1"


class NeuroticismAnalytics(BaseAnalytics):
    def __init__(self) -> None:
        self.values = {trait: 0 for trait in NeuroticismTrait}

    @property
    def percentages(self) -> dict[NeuroticismTrait, float]:
        return {
            NeuroticismTrait.N1: (
                (
                    self.values[NeuroticismTrait.N1]
                    / (self.values[NeuroticismTrait.N1] + self.values[NeuroticismTrait.S1])
                )
                * 100
                if self.values[NeuroticismTrait.N1] + self.values[NeuroticismTrait.S1] > 0
                else 0
            ),
            NeuroticismTrait.S1: (
                (
                    self.values[NeuroticismTrait.S1]
                    / (self.values[NeuroticismTrait.N1] + self.values[NeuroticismTrait.S1])
                )
                * 100
                if self.values[NeuroticismTrait.N1] + self.values[NeuroticismTrait.S1] > 0
                else 0
            ),
        }

    def add(self, trait: NeuroticismTrait, value: int, max_value: int) -> None:
        if trait in NeuroticismTrait:
            self.values[trait] += value

    def to_schema(self) -> Analytics:
        items = [
            Analytics.ScoreItem(
                name=trait.value,
                value=self.values[trait],
                percentage=self.percentages[trait],
                categories=[trait.name],
            )
            for trait in NeuroticismTrait
        ]
        return Analytics(
            name=self.__class__.__name__,
            items=items,
            extra={},
        )
