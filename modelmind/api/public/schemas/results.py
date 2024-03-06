from datetime import datetime

from modelmind.models.results.base import ResultData

from .base import BaseResponse


class ResultsResponse(BaseResponse):
    id: str
    data: ResultData
    created_at: datetime
