from enum import StrEnum

from modelmind.community.theory.jung.functions import JungFunction
from modelmind.community.theory.mbti.trait import MBTITrait


class ClassVar:
    def __init__(self, value) -> None:  # type: ignore
        self.value = value

    def __get__(self, *args):  # type: ignore
        return self.value

    def __set__(self, _, value) -> None:  # type: ignore
        self.value = value


class PersonyDimension(StrEnum):
    PREFERENCE_IE = "P-IE"
    PREFERENCE_NS = "P-NS"
    PREFERENCE_TF = "P-TF"
    PREFERENCE_JP = "P-JP"
    LIFESTYLE_NINE = "L-NINE"
    LIFESTYLE_SISE = "L-SISE"
    LIFESTYLE_TETI = "L-TETI"
    LIFESTYLE_FEFI = "L-FEFI"
    TEMPERAMENT_NISI = "T-NISI"
    TEMPERAMENT_NESE = "T-NESE"
    TEMPERAMENT_TEFE = "T-TEFE"
    TEMPERAMENT_TIFI = "T-TIFI"
    ATTITUDE_INJ = "A-INJ"
    ATTITUDE_ISJ = "A-ISJ"
    ATTITUDE_ITP = "A-ITP"
    ATTITUDE_IFP = "A-IFP"
    ATTITUDE_ETJ = "A-ETJ"
    ATTITUDE_EFJ = "A-EFJ"
    ATTITUDE_ENP = "A-ENP"
    ATTITUDE_ESP = "A-ESP"

    _category_data = ClassVar(
        {
            "PREFERENCE_IE": {"lowTrait": MBTITrait.I, "highTrait": MBTITrait.E},
            "PREFERENCE_NS": {"lowTrait": MBTITrait.N, "highTrait": MBTITrait.S},
            "PREFERENCE_TF": {"lowTrait": MBTITrait.T, "highTrait": MBTITrait.F},
            "PREFERENCE_JP": {"lowTrait": MBTITrait.J, "highTrait": MBTITrait.P},
            "LIFESTYLE_NINE": {
                "lowTrait": MBTITrait.J,
                "highTrait": MBTITrait.P,
                "lowFunction": JungFunction.Ni,
                "highFunction": JungFunction.Ne,
            },
            "LIFESTYLE_SISE": {
                "lowTrait": MBTITrait.J,
                "highTrait": MBTITrait.P,
                "lowFunction": JungFunction.Si,
                "highFunction": JungFunction.Se,
            },
            "LIFESTYLE_TETI": {
                "lowTrait": MBTITrait.J,
                "highTrait": MBTITrait.P,
                "lowFunction": JungFunction.Te,
                "highFunction": JungFunction.Ti,
            },
            "LIFESTYLE_FEFI": {
                "lowTrait": MBTITrait.J,
                "highTrait": MBTITrait.P,
                "lowFunction": JungFunction.Fe,
                "highFunction": JungFunction.Fi,
            },
            "TEMPERAMENT_NISI": {
                "lowTrait": MBTITrait.N,
                "highTrait": MBTITrait.S,
                "lowFunction": JungFunction.Ni,
                "highFunction": JungFunction.Si,
            },
            "TEMPERAMENT_NESE": {
                "lowTrait": MBTITrait.N,
                "highTrait": MBTITrait.S,
                "lowFunction": JungFunction.Ne,
                "highFunction": JungFunction.Se,
            },
            "TEMPERAMENT_TEFE": {
                "lowTrait": MBTITrait.T,
                "highTrait": MBTITrait.F,
                "lowFunction": JungFunction.Te,
                "highFunction": JungFunction.Fe,
            },
            "TEMPERAMENT_TIFI": {
                "lowTrait": MBTITrait.T,
                "highTrait": MBTITrait.F,
                "lowFunction": JungFunction.Ti,
                "highFunction": JungFunction.Fi,
            },
            "ATTITUDE_INJ": {
                "lowTrait": MBTITrait.E,
                "highTrait": MBTITrait.I,
                "lowFunction": JungFunction.Se,
                "highFunction": JungFunction.Ni,
            },
            "ATTITUDE_ISJ": {
                "lowTrait": MBTITrait.E,
                "highTrait": MBTITrait.I,
                "lowFunction": JungFunction.Ne,
                "highFunction": JungFunction.Si,
            },
            "ATTITUDE_ITP": {
                "lowTrait": MBTITrait.E,
                "highTrait": MBTITrait.I,
                "lowFunction": JungFunction.Fe,
                "highFunction": JungFunction.Ti,
            },
            "ATTITUDE_IFP": {
                "lowTrait": MBTITrait.E,
                "highTrait": MBTITrait.I,
                "lowFunction": JungFunction.Te,
                "highFunction": JungFunction.Fi,
            },
            "ATTITUDE_ETJ": {
                "lowTrait": MBTITrait.I,
                "highTrait": MBTITrait.E,
                "lowFunction": JungFunction.Fi,
                "highFunction": JungFunction.Te,
            },
            "ATTITUDE_EFJ": {
                "lowTrait": MBTITrait.I,
                "highTrait": MBTITrait.E,
                "lowFunction": JungFunction.Ti,
                "highFunction": JungFunction.Fe,
            },
            "ATTITUDE_ENP": {
                "lowTrait": MBTITrait.I,
                "highTrait": MBTITrait.E,
                "lowFunction": JungFunction.Si,
                "highFunction": JungFunction.Ne,
            },
            "ATTITUDE_ESP": {
                "lowTrait": MBTITrait.I,
                "highTrait": MBTITrait.E,
                "lowFunction": JungFunction.Ni,
                "highFunction": JungFunction.Se,
            },
        },
    )

    @property
    def data(self) -> dict[str, MBTITrait | JungFunction]:
        return self._category_data[self.name]

    @property
    def data_traits(self) -> dict[str, MBTITrait]:
        return {k: v for k, v in self.data.items() if isinstance(v, MBTITrait)}

    @property
    def data_functions(self) -> dict[str, JungFunction]:
        return {k: v for k, v in self.data.items() if isinstance(v, JungFunction)}

    @property
    def high_trait(self) -> MBTITrait | None:
        return self.data_traits.get("highTrait")

    @property
    def low_trait(self) -> MBTITrait | None:
        return self.data_traits.get("lowTrait")

    @property
    def low_function(self) -> JungFunction | None:
        return self.data_functions.get("lowFunction")

    @property
    def high_function(self) -> JungFunction | None:
        return self.data_functions.get("highFunction")

    @property
    def has_function(self) -> bool:
        return self.low_function is not None or self.high_function is not None

    @classmethod
    def preferences(cls) -> list[str]:
        return [
            cls.PREFERENCE_IE,
            cls.PREFERENCE_NS,
            cls.PREFERENCE_TF,
            cls.PREFERENCE_JP,
        ]

    @classmethod
    def lifestyles(cls) -> list[str]:
        return [
            cls.LIFESTYLE_NINE,
            cls.LIFESTYLE_SISE,
            cls.LIFESTYLE_TETI,
            cls.LIFESTYLE_FEFI,
        ]

    @classmethod
    def temperaments(cls) -> list[str]:
        return [
            cls.TEMPERAMENT_NISI,
            cls.TEMPERAMENT_NESE,
            cls.TEMPERAMENT_TEFE,
            cls.TEMPERAMENT_TIFI,
        ]

    @classmethod
    def attitudes(cls) -> list[str]:
        return [
            cls.ATTITUDE_INJ,
            cls.ATTITUDE_ISJ,
            cls.ATTITUDE_ITP,
            cls.ATTITUDE_IFP,
            cls.ATTITUDE_ETJ,
            cls.ATTITUDE_EFJ,
            cls.ATTITUDE_ENP,
            cls.ATTITUDE_ESP,
        ]
