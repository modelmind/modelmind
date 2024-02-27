
from .base import BaseResponse

# TODO: we may want to decouple the response schema from the domain model
# Use an analytics response builder/factory?


class AnalyticsResponse(BaseResponse):
    analytics: list[dict]
