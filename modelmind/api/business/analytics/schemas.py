from modelmind.api.business.schemas import BaseResponse
from modelmind.models.analytics.schemas import Analytics

# TODO: we may want to decouple the response schema from the domain model
# Use an analytics response builder/factory?


class AnalyticsResponse(BaseResponse):
    analytics: list[Analytics]
