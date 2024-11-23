from datetime import datetime
from enum import StrEnum

from modelmind.api.business.schemas import BaseResponse
from modelmind.models.results.base import ResultData


class ResultVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class ResultsResponse(BaseResponse):
    id: str
    questionnaire_id: str
    session_id: str
    profile_id: str
    data: ResultData
    created_at: datetime
    visibility: ResultVisibility
    label: str | None = None
    language: str | None = None
