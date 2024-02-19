from enum import StrEnum



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
            "PREFERENCE_IE": {"value": "P-IE", "negtrait": "I", "postrait": "E"},
            "PREFERENCE_NS": {"value": "P-NS", "negtrait": "N", "postrait": "S"},
            "PREFERENCE_TF": {"value": "P-TF", "negtrait": "T", "postrait": "F"},
            "PREFERENCE_JP": {"value": "P-JP", "negtrait": "J", "postrait": "P"},
            "LIFESTYLE_NINE": {
                "value": "L-NINE",
                "negtrait": "J",
                "postrait": "P",
                "negfunc": "Ni",
                "posfunc": "Ne",
            },
            "LIFESTYLE_SISE": {
                "value": "L-SISE",
                "negtrait": "J",
                "postrait": "P",
                "negfunc": "Si",
                "posfunc": "Se",
            },
            "LIFESTYLE_TETI": {
                "value": "L-TETI",
                "negtrait": "J",
                "postrait": "P",
                "negfunc": "Te",
                "posfunc": "Ti",
            },
            "LIFESTYLE_FEFI": {
                "value": "L-FEFI",
                "negtrait": "J",
                "postrait": "P",
                "negfunc": "Fe",
                "posfunc": "Fi",
            },
            "TEMPERAMENT_NISI": {
                "value": "T-NISI",
                "negtrait": "N",
                "postrait": "S",
                "negfunc": "Ni",
                "posfunc": "Si",
            },
            "TEMPERAMENT_NESE": {
                "value": "T-NESE",
                "negtrait": "N",
                "postrait": "S",
                "negfunc": "Ne",
                "posfunc": "Se",
            },
            "TEMPERAMENT_TEFE": {
                "value": "T-TEFE",
                "negtrait": "T",
                "postrait": "F",
                "negfunc": "Te",
                "posfunc": "Fe",
            },
            "TEMPERAMENT_TIFI": {
                "value": "T-TIFI",
                "negtrait": "T",
                "postrait": "F",
                "negfunc": "Ti",
                "posfunc": "Fi",
            },
            "ATTITUDE_INJ": {
                "value": "A-INJ",
                "negtrait": "E",
                "postrait": "I",
                "negfunc": "Se",
                "posfunc": "Ni",
            },
            "ATTITUDE_ISJ": {
                "value": "A-ISJ",
                "negtrait": "E",
                "postrait": "I",
                "negfunc": "Ne",
                "posfunc": "Si",
            },
            "ATTITUDE_ITP": {
                "value": "A-ITP",
                "negtrait": "E",
                "postrait": "I",
                "negfunc": "Fe",
                "posfunc": "Ti",
            },
            "ATTITUDE_IFP": {
                "value": "A-IFP",
                "negtrait": "E",
                "postrait": "I",
                "negfunc": "Te",
                "posfunc": "Fi",
            },
            "ATTITUDE_ETJ": {
                "value": "A-ETJ",
                "negtrait": "I",
                "postrait": "E",
                "negfunc": "Fi",
                "posfunc": "Te",
            },
            "ATTITUDE_EFJ": {
                "value": "A-EFJ",
                "negtrait": "I",
                "postrait": "E",
                "negfunc": "Ti",
                "posfunc": "Fe",
            },
            "ATTITUDE_ENP": {
                "value": "A-ENP",
                "negtrait": "I",
                "postrait": "E",
                "negfunc": "Si",
                "posfunc": "Ne",
            },
            "ATTITUDE_ESP": {
                "value": "A-ESP",
                "negtrait": "I",
                "postrait": "E",
                "negfunc": "Ni",
                "posfunc": "Se",
            },
        },
    )

    @property
    def data(self) -> dict[str, str]:
        return self._category_data[self.name]

    @property
    def postrait(self) -> str:
        return self.data["postrait"]

    @property
    def negtrait(self) -> str:
        return self.data["negtrait"]

    @property
    def negfunc(self) -> str | None:
        return self.data["negfunc"] if "negfunc" in self.data else None

    @property
    def posfunc(self) -> str | None:
        return self.data["posfunc"] if "posfunc" in self.data else None

    @property
    def step(self) -> str:
        return self.name.split("_")[0]

    @classmethod
    def steps(cls) -> list[str]:
        return list(c.step for c in cls)
