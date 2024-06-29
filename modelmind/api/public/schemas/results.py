from datetime import datetime
from enum import StrEnum

from modelmind.models.results.base import ResultData

from .base import BaseResponse


class ResultVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class ResultsResponse(BaseResponse):
    id: str
    questionnaire_id: str
    session_id: str
    data: ResultData
    created_at: datetime
    visibility: ResultVisibility
    label: str | None = None
