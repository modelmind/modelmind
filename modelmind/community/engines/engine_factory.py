from enum import StrEnum
from typing import Type
from modelmind.models.engines.base import BaseEngine
from .persony import PersonyEngineV1


class EngineName(StrEnum):
    PERSONY_V1 = "persony-v1"


class EngineFactory:

    engine_map = {
        EngineName.PERSONY_V1: PersonyEngineV1
    }

    @classmethod
    def get_engine(cls, engine_name: str) -> Type[BaseEngine]:
        try:
            return cls.engine_map[EngineName(engine_name)]
        except KeyError:
            raise ValueError(f"Engine {engine_name} not supported yet.")
