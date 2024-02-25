from enum import StrEnum
from typing import Type

from modelmind.models.engines.base import Engine

from .persony import PersonyEngineV1


class EngineName(StrEnum):
    PERSONY_V1 = "persony-v1"


class EngineFactory:
    engine_map = {EngineName.PERSONY_V1: PersonyEngineV1}

    @classmethod
    def get_engine(cls, engine_name: str) -> Type[Engine]:
        try:
            return cls.engine_map[EngineName(engine_name)]
        except KeyError:
            raise ValueError(f"Engine {engine_name} not supported yet.")

    @classmethod
    def get_available_engine_names(cls) -> list[str]:
        return list(cls.engine_map.keys())
