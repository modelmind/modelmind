from modelmind.models.analytics.schemas import Analytics

from .base import BaseResponse

# TODO: we may want to decouple the response schema from the domain model
# Use an analytics response builder/factory?


class AnalyticsResponse(BaseResponse):
    analytics: list[Analytics]
