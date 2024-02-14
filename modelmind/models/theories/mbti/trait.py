from enum import Enum

from pydantic import BaseModel

from .types import MBTIType


class Trait(Enum):
    I = "I"
    E = "E"
    N = "N"
    S = "S"
    T = "T"
    F = "F"
    J = "J"
    P = "P"


class MBTITraits(BaseModel):
    I: int = 0
    E: int = 0
    N: int = 0
    S: int = 0
    T: int = 0
    F: int = 0
    J: int = 0
    P: int = 0

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

    @property
    def dominants(self) -> str:
        return "".join(
            [
                "E" if self.E > self.I else "I",
                "S" if self.S > self.N else "N",
                "T" if self.T > self.F else "F",
                "J" if self.J > self.P else "P",
            ],
        )

    @property
    def percentages(self) -> dict[str, float]:
        return {
            "I": (self.I / (self.I + self.E)) * 100,
            "E": (self.E / (self.I + self.E)) * 100,
            "N": (self.N / (self.N + self.S)) * 100,
            "S": (self.S / (self.N + self.S)) * 100,
            "T": (self.T / (self.T + self.F)) * 100,
            "F": (self.F / (self.T + self.F)) * 100,
            "J": (self.J / (self.J + self.P)) * 100,
            "P": (self.P / (self.J + self.P)) * 100,
        }

    def get_opposite_trait(self, trait: str) -> str:
        opposites = {
            "I": "E",
            "E": "I",
            "N": "S",
            "S": "N",
            "T": "F",
            "F": "T",
            "J": "P",
            "P": "J",
        }
        return opposites.get(trait, trait)

    def add(self, trait_name: str, value: int) -> None:
        if trait_name in self.model_fields:
            setattr(self, trait_name, getattr(self, trait_name) + value)
        else:
            raise ValueError(f"Trait {trait_name} not recognized.")

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
