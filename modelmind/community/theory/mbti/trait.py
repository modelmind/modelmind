from enum import StrEnum
from modelmind.models.analytics.base import BaseAnalytics

from .types import MBTIType


class MBTITrait(StrEnum):
    I = "I"
    E = "E"
    N = "N"
    S = "S"
    T = "T"
    F = "F"
    J = "J"
    P = "P"


class MBTITraitsAnalytics(BaseAnalytics):

    def __init__(self) -> None:

        self.I: int = 0
        self.E: int = 0
        self.N: int = 0
        self.S: int = 0
        self.T: int = 0
        self.F: int = 0
        self.J: int = 0
        self.P: int = 0

    @property
    def dominants(self) -> MBTIType:
        return MBTIType("".join(
            [
                MBTITrait.E if self.E > self.I else MBTITrait.I,
                MBTITrait.S if self.S > self.N else MBTITrait.N,
                MBTITrait.T if self.T > self.F else MBTITrait.F,
                MBTITrait.J if self.J > self.P else MBTITrait.P,
            ],
        ))

    @property
    def percentages(self) -> dict[str, float]:
        return {
            MBTITrait.I: (self.I / (self.I + self.E)) * 100,
            MBTITrait.E: (self.E / (self.I + self.E)) * 100,
            MBTITrait.N: (self.N / (self.N + self.S)) * 100,
            MBTITrait.S: (self.S / (self.N + self.S)) * 100,
            MBTITrait.T: (self.T / (self.T + self.F)) * 100,
            MBTITrait.F: (self.F / (self.T + self.F)) * 100,
            MBTITrait.J: (self.J / (self.J + self.P)) * 100,
            MBTITrait.P: (self.P / (self.J + self.P)) * 100,
        }

    def get_opposite_trait(self, trait: MBTITrait) -> MBTITrait:
        opposites = {
            MBTITrait.I: MBTITrait.E,
            MBTITrait.E: MBTITrait.I,
            MBTITrait.N: MBTITrait.S,
            MBTITrait.S: MBTITrait.N,
            MBTITrait.T: MBTITrait.F,
            MBTITrait.F: MBTITrait.T,
            MBTITrait.J: MBTITrait.P,
            MBTITrait.P: MBTITrait.J,
        }
        return opposites.get(trait, trait)

    def add(self, trait_name: MBTITrait, value: int) -> None:
        setattr(self, trait_name, getattr(self, trait_name) + value)

    def compute_mbti_probabilities(self) -> dict[str, float]:

        mbti_types = list(MBTIType.__members__.keys())

        # Calculate probabilities based on the trait scores
        probabilities = {}
        for mbti in mbti_types:
            p = 1.0
            for letter in mbti:
                p *= (
                    self.percentages[letter] / 100
                )  # Convert the percentage to a proportion
            probabilities[mbti] = p

        # Normalize the probabilities so they sum to 1
        total = sum(probabilities.values())
        for mbti in probabilities:
            probabilities[mbti] /= total

        return probabilities

    # Alias properties
    @property
    def introversion(self) -> int:
        return self.I

    @introversion.setter
    def introversion(self, value: int) -> None:
        self.I = value

    @property
    def extraversion(self) -> int:
        return self.E

    @extraversion.setter
    def extraversion(self, value: int) -> None:
        self.E = value

    @property
    def intuition(self) -> int:
        return self.N

    @intuition.setter
    def intuition(self, value: int) -> None:
        self.N = value

    @property
    def sensing(self) -> int:
        return self.S

    @sensing.setter
    def sensing(self, value: int) -> None:
        self.S = value

    @property
    def thinking(self) -> int:
        return self.T

    @thinking.setter
    def thinking(self, value: int) -> None:
        self.T = value

    @property
    def feeling(self) -> int:
        return self.F

    @feeling.setter
    def feeling(self, value: int) -> None:
        self.F = value

    @property
    def judging(self) -> int:
        return self.J

    @judging.setter
    def judging(self, value: int) -> None:
        self.J = value

    @property
    def perceiving(self) -> int:
        return self.P

    @perceiving.setter
    def perceiving(self, value: int) -> None:
        self.P = value



class MBTITraitException(Exception):
    pass
