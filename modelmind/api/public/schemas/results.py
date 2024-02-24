from modelmind.models.results.base import ResultData

from .base import BaseResponse


class ResultsResponse(BaseResponse):
    data: ResultData
