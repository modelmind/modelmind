from typing import Literal, TypedDict, Union

from pydantic import Field

from modelmind.db.schemas import DBIdentifier, DBObject


class Accuracy(TypedDict):
    confidence_level: Literal["total", ">=1", ">=2", ">=3", ">=4"] | str
    total_predictions: int
    correct_predictions: int
    accuracy_percentage: float


class PersonyStatistics(TypedDict):
    type: Literal["persony"]

    accuracy: list[Accuracy]


StatisticsData = Union[PersonyStatistics]


class DBStatistics(DBObject):
    questionnaire_id: DBIdentifier
    data: StatisticsData = Field(..., discriminator="type")
