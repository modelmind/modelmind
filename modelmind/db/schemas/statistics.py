from typing import Literal, TypedDict, Union

from pydantic import Field

from modelmind.db.schemas import DBIdentifier, DBObject


class Accuracy(TypedDict):
    total_predictions: int
    correct_predictions: int
    percentage: float


class AccuracyMetric(TypedDict):
    total: Accuracy
    confidence_ge_1: Accuracy
    confidence_ge_2: Accuracy
    confidence_ge_3: Accuracy
    confidence_ge_4: Accuracy


class CountsMetric(TypedDict):
    total: int
    with_label: int
    male: int
    female: int
    other: int


class PersonyStatistics(TypedDict):
    type: Literal["persony"]

    accuracy: AccuracyMetric
    counts: CountsMetric


StatisticsData = Union[PersonyStatistics]


class DBStatistics(DBObject):
    questionnaire_id: DBIdentifier
    data: StatisticsData = Field(..., discriminator="type")
